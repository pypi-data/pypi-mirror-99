# -*- coding: utf-8 -*-
import os
import glob

from time import strftime
import json
from flask import Blueprint, render_template, redirect, url_for, flash, \
    request, jsonify, session, current_app
from flask import current_app as app
from flask_login import login_required
from flask_login import current_user
from werkzeug.utils import secure_filename
from celery.result import AsyncResult


from clustermgr.extensions import db, wlogger, csrf
from clustermgr.models import AppConfiguration, Server  # , KeyRotation
from clustermgr.forms import AppConfigForm, SchemaForm, \
    TestUser, InstallServerForm, LdapSchema  # , KeyRotationForm

from celery.result import AsyncResult

from clustermgr.core.clustermgr_logging import sys_logger as logger

from clustermgr.core.ldap_functions import LdapOLC
from wtforms.validators import DataRequired

from clustermgr.tasks.cluster import upgrade_clustermgr_task
from clustermgr.core.license import license_reminder
from clustermgr.extensions import celery
from clustermgr.core.license import prompt_license, license_required

from clustermgr.core.remote import RemoteClient, FakeRemote, ClientNotSetupException

from clustermgr.core.clustermgr_installer import Installer

from clustermgr.core.utils import get_setup_properties, \
    get_opendj_replication_status, as_boolean, get_enabled_services, encode

from clustermgr.tasks.server import collect_server_details, set_up_ldap_cache_cleaner


index = Blueprint('index', __name__)
index.before_request(prompt_license)
index.before_request(license_reminder)
index.before_request(license_required)

msg_text = ''

@index.route('/')
def home():
    
    if not current_user.is_authenticated:    
        return redirect(url_for("auth.login", next='/'))

    """This is the home view --dashboard--"""
    if 'nongluuldapinfo' in session:
        del session['nongluuldapinfo']
    
    try:
        appconf = AppConfiguration.query.first()
    except:
        return render_template('index_nodb.html')
    
    if not appconf:
        return render_template('intro.html', setup='cluster')

    servers = Server.query.all()
    if not servers:
        return render_template('intro.html', setup='server')


    ask_passphrase = False
    c = RemoteClient(servers[0].ip, servers[0].hostname, ssh_port=servers[0].ssh_port)
    try:
        c.startup()
    
    except ClientNotSetupException as e:

        if str(e) == 'Pubkey is encrypted.':
            ask_passphrase = True
            flash("Pubkey seems to password protected. "
                "Please set passphrase.",
                'warning')
        elif str(e) == 'Could not deserialize key data.':
            ask_passphrase = True
            flash("Password you provided for pubkey did not work. "
                "Please set valid passphrase.",
                'warning')
        else:
            flash("SSH connection to {} failed. Please check if your pub key is "
                "added to /root/.ssh/authorized_keys on this server. Reason: {}".format(
                                                servers[0].hostname, e), 'error')

        if ask_passphrase:
            return render_template('index_passphrase.html', e=e, 
                ask_passphrase=ask_passphrase, next='/',
                warning_text="Error accessing primary server")
    
    service_update_period = 300
    
    if appconf.ldap_update_period:
        service_update_period = appconf.ldap_update_period
        if appconf.ldap_update_period_unit != 's':
            service_update_period = service_update_period * 60


    server_id_list = [str(server.id) for server in servers]
    services = get_enabled_services()

    return render_template('dashboard.html', servers=servers, app_conf=appconf,
                             services=services, server_id_list=server_id_list,
                             service_update_period=service_update_period
                        )

@index.route('/configuration/', methods=['GET', 'POST'])
@login_required
def app_configuration():
    """This view provides application configuration forms"""

    # create forms
    conf_form = AppConfigForm()
    sch_form = SchemaForm()
    config = AppConfiguration.query.first()
    schemafiles = os.listdir(app.config['SCHEMA_DIR'])

    prop = get_setup_properties()
    
    repo_list = glob.glob(os.path.join(app.config['GLUU_REPO'],'gluu-server*'))
    
    if repo_list:
        conf_form.gluu_archive.choices = [ ('', ' -- Select -- ')]
        for f in repo_list:
            conf_form.gluu_archive.choices.append((f,os.path.split(f)[1]))
    
        if request.method == 'GET' and config:
            conf_form.gluu_archive.data = config.gluu_archive

    # If the form is submitted and password for replication user was not
    # not supplied, make password "**dummy**", so don't change
    # what we have before

    #external_lb_checked = False
    external_lb_checked = conf_form.external_load_balancer.data
    
    if request.method == 'POST':
        if conf_form.offline.data:
            conf_form.gluu_archive.validators = [ DataRequired() ]        

        if config and not conf_form.replication_pw.data.strip():
            conf_form.replication_pw.validators = []
            conf_form.replication_pw_confirm.validators = []
            
        if conf_form.external_load_balancer.data:
            conf_form.nginx_ip.validators= []


        if not conf_form.offline.data:
            del conf_form._fields['gluu_archive']

    if not config:
        #del conf_form.replication_pw
        #del conf_form.replication_pw_confirm
        config = AppConfiguration(use_ldap_cache=True)
        db.session.add(config)

    # If form is submitted and validated process it
    if conf_form.update.data and conf_form.validate_on_submit():
        if config.replication_pw:
            new_replication_passwd = conf_form.replication_pw.data.strip()
            if conf_form.replication_pw.data:

                c = None
                server = Server.query.first()
                
                if server:
                
                    c = RemoteClient(server.hostname, ip=server.ip, ssh_port=server.ssh_port)
                    
                    try:
                        c.startup()
                    except Exception as e:
                        flash("Can't establish SSH connection to {}. "
                              "Replication password is not changed".format(
                              server.hostname),
                                "warning")
                    if c:
     
                        installer = Installer(c, config.gluu_version, server.os, ssh_port=server.ssh_port)
                    
                        cmd = ('/opt/opendj/bin/ldappasswordmodify --bindDN '
                        '\'cn=Directory Manager\' --bindPassword $\'{}\' '
                        '--port 4444 --newPassword $\'{}\' --authzID '
                        '\'cn=admin,cn=Administrators,cn=admin data\' '
                        '--trustAll --useSSL'.format(
                        ))

                        result = installer.run(cmd)
                        if result[1].strip() == \
                        'The LDAP password modify operation was successful':
                            flash("Replication password is changed", "success")
                            config.replication_pw = new_replication_passwd
 
        
        config.gluu_version = conf_form.gluu_version.data.strip()
        config.nginx_host = conf_form.nginx_host.data.strip()
        config.nginx_ip = conf_form.nginx_ip.data.strip()
        config.nginx_ssh_port = conf_form.nginx_ssh_port.data
        config.modify_hosts = conf_form.modify_hosts.data
        
        config.ldap_update_period = conf_form.ldap_update_period.data
        config.ldap_update_period_unit = 's'
        config.external_load_balancer = conf_form.external_load_balancer.data
        config.ldap_cache_clean_period = int(conf_form.ldap_cache_clean_period.data)

        if as_boolean(prop['installSaml']):
            config.use_ldap_cache = True
        else:
            config.use_ldap_cache = conf_form.use_ldap_cache.data


        if conf_form.offline.data:
            config.offline = True
            config.gluu_archive = conf_form.gluu_archive.data
        else:
            config.offline = False
            config.gluu_archive = ''

    
        if getattr(conf_form, 'replication_pw'):
            if conf_form.replication_pw_confirm.data:
                config.replication_pw = conf_form.replication_pw.data.strip()
    
        config.gluu_version = conf_form.gluu_version.data.strip()

        db.session.commit()

        flash("Gluu Cluster Manager configuration has been updated.", "success")

        collect_server_details.delay(-1)

        primary_server = Server.query.filter_by(primary_server=True).first()

        if primary_server:

            installer = Installer(
                                    primary_server,
                                    config.gluu_version,
                                    logger_task_id=0,
                                    server_os=primary_server.os,
                                    ssh_port=primary_server.ssh_port
                                )

            if not installer.conn:
                flash("Primary server is reachable via ssh.", 'warning')
            else:
                set_up_ldap_cache_cleaner(installer, config.ldap_cache_clean_period)

        if request.args.get('next'):
            return redirect(request.args.get('next'))

    elif sch_form.upload.data and sch_form.validate_on_submit():
        f = sch_form.schema.data
        filename = secure_filename(f.filename)
        if any(filename in s for s in schemafiles):
            name, extension = os.path.splitext(filename)
            matches = [s for s in schemafiles if name in s]
            filename = name + "_" + str(len(matches)) + extension
        f.save(os.path.join(app.config['SCHEMA_DIR'], filename))
        schemafiles.append(filename)
        flash("Schema: {0} has been uploaded sucessfully. "
              "Please edit slapd.conf of primary server and "
              "re-deploy all servers.".format(filename),
              "success")

    # request.method == GET gets processed here
    if config: #and config.replication_dn:
        #conf_form.replication_dn.data = config.replication_dn.replace(
        #    "cn=", "").replace(",o=gluu", "")
        #conf_form.replication_pw.data = config.replication_pw
        conf_form.nginx_host.data = config.nginx_host
        conf_form.modify_hosts.data = config.modify_hosts
        conf_form.nginx_ip.data = config.nginx_ip
        conf_form.nginx_ssh_port.data = config.nginx_ssh_port
        conf_form.external_load_balancer.data = config.external_load_balancer
        conf_form.use_ldap_cache.data = config.use_ldap_cache
        conf_form.offline.data =  config.offline
        conf_form.ldap_cache_clean_period.data = str(config.ldap_cache_clean_period)
        
        if not conf_form.nginx_ssh_port.data:
            conf_form.nginx_ssh_port.data = 22
        
        #if config.external_load_balancer:
        #    conf_form.cache_host.data = config.cache_host
        #    conf_form.cache_ip.data = config.cache_ip
        
        
        service_status_update_period = config.ldap_update_period

        if service_status_update_period and config.ldap_update_period_unit != 's':
                service_status_update_period = service_status_update_period * 60         
        
        if not service_status_update_period:
            service_status_update_period = 300
        
        conf_form.ldap_update_period.data = str(service_status_update_period)
        
        #conf_form.use_ip.data = config.use_ip
        if config.gluu_version:
            conf_form.gluu_version.data = config.gluu_version

    #create fake remote class that provides the same interface with RemoteClient
    fc = FakeRemote()
    
    #Getermine local OS type
    localos = fc.get_os_type()


    return render_template('app_config.html', cform=conf_form, sform=sch_form,
                        config=config, schemafiles=schemafiles, localos=localos,
                        external_lb_checked=external_lb_checked,
                        repo_dir = app.config['GLUU_REPO'],
                        installSaml=as_boolean(prop['installSaml']),
                        next=request.args.get('next'))


# @index.route("/key_rotation", methods=["GET", "POST"])
# def key_rotation():
#     kr = KeyRotation.query.first()
#     form = KeyRotationForm()
#     oxauth_servers = [server for server in Server.query]

#     if request.method == "GET" and kr is not None:
#         form.interval.data = kr.interval
#         form.type.data = kr.type
#         form.oxeleven_url.data = kr.oxeleven_url
#         form.inum_appliance.data = kr.inum_appliance

#     if form.validate_on_submit():
#         if not kr:
#             kr = KeyRotation()

#         kr.interval = form.interval.data
#         kr.type = form.type.data
#         kr.oxeleven_url = form.oxeleven_url.data
#         kr.inum_appliance = form.inum_appliance.data
#         kr.oxeleven_token_key = generate_random_key()
#         kr.oxeleven_token_iv = generate_random_iv()
#         kr.oxeleven_token = encrypt_text(
#             b"{}".format(form.oxeleven_token.data),
#             kr.oxeleven_token_key,
#             kr.oxeleven_token_iv,
#         )
#         db.session.add(kr)
#         db.session.commit()
#         # rotate the keys immediately
#         rotate_pub_keys.delay()
#         return redirect(url_for("key_rotation"))
#     return render_template("key_rotation.html",
#                            form=form,
#                            rotation=kr,
#                            oxauth_servers=oxauth_servers)


# @index.route("/api/oxauth_server", methods=["GET", "POST"])
# def oxauth_server():
#     if request.method == "POST":
#         hostname = request.form.get("hostname")
#         gluu_server = request.form.get("gluu_server")

#         if gluu_server == "true":
#             gluu_server = True
#         else:
#             gluu_server = False

#         if not hostname:
#             return jsonify({
#                 "status": 400,
#                 "message": "Invalid data",
#                 "params": "hostname can't be empty",
#             }), 400

#         server = Server()
#         server.hostname = hostname
#         server.gluu_server = gluu_server
#         db.session.add(server)
#         db.session.commit()
#         return jsonify({
#             "id": server.id,
#             "hostname": server.hostname,
#             "gluu_server": server.gluu_server,
#         }), 201

#     servers = [{
#         "id": srv.id,
#         "hostname": srv.hostname,
#         "gluu_server": srv.gluu_server,
#     } for srv in Server.query]
#     return jsonify(servers)


# @index.route("/api/oxauth_server/<id>", methods=["POST"])
# def delete_oxauth_server(id):
#     server = Server.query.get(id)
#     if server:
#         db.session.delete(server)
#         db.session.commit()
#     return jsonify({}), 204




@index.route('/log/<task_id>')
@login_required
def get_log(task_id):
    
    global msg_text
    
    msgs = wlogger.get_messages(task_id)
    result = AsyncResult(id=task_id, app=celery)
    value = 0
    
    error_message = ''

    if result.result != None:
        if getattr(result, 'traceback'):
            error_message = str(result.traceback)
            
    if result.state == 'SUCCESS' or result.state == 'FAILED':
        if result.result:
            if type(result.result) != type(True):
                try:
                    value = result.result.message
                except:
                    value = result.result
        wlogger.clean(task_id)
    log = {'task_id': task_id, 'state': result.state, 'messages': msgs,
           'result': value, 'error_message': error_message}

    ts = strftime('[%Y-%b-%d %H:%M]')
    
    log_ = False
    
    if msgs:
        if msgs[-1].get('msg','') != msg_text:
            
            msg_text = msgs[-1].get('msg','')
            log_ = True
    
    if log_ or error_message:
        
        logger.error('%s [Celery] %s %s %s %s',
                          ts,
                          result.state,
                          msg_text,
                          value,
                          error_message
                    )

    return jsonify(log)


@index.route('/mmr/')
@login_required
def multi_master_replication():
    """Multi Master Replication view for OpenDJ"""

    # Check if replication user (dn) and password has been configured
    app_config = AppConfiguration.query.first()
    ldaps = Server.query.all()
    primary_server = Server.query.filter_by(primary_server=True).first()
    if not app_config:
        flash("Repication user and/or password has not been defined."
              " Please go to 'Configuration' and set these before proceed.",
              "warning")
        return redirect(url_for('index.home'))

    if not ldaps:
        flash("Servers has not been added. "
              "Please add servers",
              "warning")
        return redirect(url_for('index.home'))


    ldap_errors = []

    prop = get_setup_properties()

    rep_status = get_opendj_replication_status()

    stat = ''
    if not rep_status[0]:
        flash(rep_status[1], "warning")
    else:
        stat = rep_status[1]
    return render_template('opendjmmr.html',
                           servers=ldaps,
                           stat = stat,
                           app_conf=app_config,
                           )

@index.route('/removecustomschema/<schema_file>')
@login_required
def remove_custom_schema(schema_file):
    """This view deletes custom schema file"""

    file_path = os.path.join(app.config['SCHEMA_DIR'], schema_file)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index.app_configuration'))



@index.route('/upgrade')
@login_required
def upgrade_clustermgr():
    """Initiates upgrading of clustermgr"""

    task = upgrade_clustermgr_task.delay()
    print "TASK STARTED", task.id
    title = "Upgrading clustermgr"
    nextpage = url_for("index.home")
    whatNext = "Go to Dashboard"
    
    return render_template('logger_single.html',
                           server_id=0,
                           title=title,
                           steps=[],
                           task=task,
                           cur_step=1,
                           auto_next=False,
                           multistep=False,
                           nextpage=nextpage,
                           whatNext=whatNext
                           )


@index.route('/setpassphrase/', methods=['POST','GET'])
@login_required
@csrf.exempt
def set_passphrase():
    passphrase = request.form['passphrase']

    encoded_passphrase = encode(os.getenv('NEW_UUID'), passphrase)

    with open(os.path.join(current_app.config['DATA_DIR'], '.pw'),'w') as f:
        f.write(encoded_passphrase)

    next_url = request.args.get('next')
    if not next_url:
        next_url = '/'
    
    return redirect(next_url)
