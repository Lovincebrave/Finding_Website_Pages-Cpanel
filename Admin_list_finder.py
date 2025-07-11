#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import threading
from queue import Queue
import time
from urllib.parse import urljoin
from colorama import init, Fore
import argparse
import sys
import os

# Initialize colorama for colored output
init()

# Full list of admin URLs provided
ADMIN_URLS = [
    "/acceso.asp", "/acceso.php", "/access/", "/access.php", "/account/", "/account.asp", 
    "/account.html", "/account.php", "/acct_login/", "/_adm_/", "/_adm/", "/adm/", 
    "/adm2/", "/adm/admloginuser.asp", "/adm/admloginuser.php", "/adm.asp", 
    "/adm_auth.asp", "/adm_auth.php", "/adm.html", "/_admin_/", "/_admin/", 
    "/admin/", "/Admin/", "/ADMIN/", "/admin1/", "/admin1.asp", "/admin1.html", 
    "/admin1.php", "/admin2/", "/admin2.asp", "/admin2.html", "/admin2/index/", 
    "/admin2/index.asp", "/admin2/index.php", "/admin2/login.asp", "/admin2/login.php", 
    "/admin2.php", "/admin3/", "/admin4/", "/admin4_account/", "/admin4_colon/", 
    "/admin5/", "/admin/account.asp", "/admin/account.html", "/admin/account.php", 
    "/admin/add_banner.php/", "/admin/addblog.php", "/admin/add_gallery_image.php", 
    "/admin/add.php", "/admin/add-room.php", "/admin/add-slider.php", 
    "/admin/add_testimonials.php", "/admin/admin/", "/admin/adminarea.php", 
    "/admin/admin.asp", "/admin/AdminDashboard.php", "/admin/admin-home.php", 
    "/admin/AdminHome.php", "/admin/admin.html", "/admin/admin_index.php", 
    "/admin/admin_login.asp", "/admin/admin-login.asp", "/admin/adminLogin.asp", 
    "/admin/admin_login.html", "/admin/admin-login.html", "/admin/adminLogin.html", 
    "/admin/admin_login.php", "/admin/admin-login.php", "/admin/adminLogin.php", 
    "/admin/admin_management.php", "/admin/admin.php", "/admin/admin_users.php", 
    "/admin/adminview.php", "/admin/adm.php", "/admin_area/", "/admin(area)/", 
    "/admin_area/admin.asp", "/adminarea/admin.asp", "/admin_area/admin.html", 
    "/adminarea/admin.html", "/admin_area/admin.php", "/adminarea/admin.php", 
    "/admin_area/index.asp", "/adminarea/index.asp", "/admin_area/index.html", 
    "/adminarea/index.html", "/admin_area/index.php", "/adminarea/index.php", 
    "/admin_area/login.asp", "/adminarea/login.asp", "/admin_area/login.html", 
    "/adminarea/login.html", "/admin_area/login.php", "/adminarea/login.php", 
    "/admin.asp", "/admin/banner.php", "/admin/banners_report.php", 
    "/admin/category.php", "/admin/change_gallery.php", "/admin/checklogin.php", 
    "/admin/configration.php", "/admincontrol.asp", "/admincontrol.html", 
    "/admincontrol/login.asp", "/admincontrol/login.html", "/admincontrol/login.php", 
    "/admin/control_pages/admin_home.php", "/admin/controlpanel.asp", 
    "/admin/controlpanel.html", "/admin/controlpanel.php", "/admincontrol.php", 
    "/admincontrol.php/", "/admin/cpanel.php", "/admin/cp.asp", "/admin/CPhome.php", 
    "/admin/cp.html", "/admincp/index.asp", "/admincp/index.html", 
    "/admincp/login.asp", "/admin/cp.php", "/admin/dashboard/index.php", 
    "/admin/dashboard.php", "/admin/dashbord.php", "/admin/dash.php", 
    "/admin/default.php", "/adm/index.asp", "/adm/index.html", "/adm/index.php", 
    "/admin/enter.php", "/admin/event.php", "/admin/form.php", "/admin/gallery.php", 
    "/admin/headline.php", "/admin/home.asp", "/admin/home.html", "/admin_home.php", 
    "/admin/home.php", "/admin.html", "/admin/index.asp", "/admin/index-digital.php", 
    "/admin/index.html", "/admin/index.php", "/admin/index_ref.php", 
    "/admin/initialadmin.php", "/administer/", "/administr8/", "/administr8.asp", 
    "/administr8.html", "/administr8.php", "/administracion.php", "/administrador/", 
    "/administratie/", "/administration/", "/administration.html", 
    "/administration.php", "/administrator", "/_administrator_/", "/_administrator/", 
    "/administrator/", "/administrator/account.asp", "/administrator/account.html", 
    "/administrator/account.php", "/administratoraccounts/", "/administrator.asp", 
    "/administrator.html", "/administrator/index.asp", "/administrator/index.html", 
    "/administrator/index.php", "/administratorlogin/", "/administrator/login.asp", 
    "/administratorlogin.asp", "/administrator/login.html", "/administrator/login.php", 
    "/administratorlogin.php", "/administrator.php", "/administrators/", 
    "/administrivia/", "/admin/leads.php", "/admin/list_gallery.php", "/admin/login", 
    "/adminLogin/", "/admin_login.asp", "/admin-login.asp", "/admin/login.asp", 
    "/adminLogin.asp", "/admin/login-home.php", "/admin_login.html", 
    "/admin-login.html", "/admin/login.html", "/adminLogin.html", "/ADMIN/login.html", 
    "/admin_login.php", "/admin-login.php", "/admin-login.php/", "/admin/login.php", 
    "/adminLogin.php", "/ADMIN/login.php", "/admin/login_success.php", 
    "/admin/loginsuccess.php", "/admin/log.php", "/admin_main.html", 
    "/admin/main_page.php", "/admin/main.php/", "/admin/ManageAdmin.php", 
    "/admin/manageImages.php", "/admin/manage_team.php", "/admin/member_home.php", 
    "/admin/moderator.php", "/admin/my_account.php", "/admin/myaccount.php", 
    "/admin-overview.php", "/admin/page_management.php", 
    "/admin/pages/home_admin.php", "/adminpanel/", "/adminpanel.asp", 
    "/adminpanel.html", "/adminpanel.php", "/admin.php", "/Admin/private/", 
    "/adminpro/", "/admin/product.php", "/admin/products.php", "/admins/", 
    "/admins.asp", "/admin/save.php", "/admins.html", "/admin/slider.php", 
    "/admin/specializations.php", "/admins.php", "/admin_tool/", "/AdminTools/", 
    "/admin/uhome.html", "/admin/upload.php", "/admin/userpage.php", 
    "/admin/viewblog.php", "/admin/viewmembers.php", "/admin/voucher.php", 
    "/AdminWeb/", "/admin/welcomepage.php", "/admin/welcome.php", 
    "/admloginuser.asp", "/admloginuser.php", "/admon/", "/ADMON/", "/adm.php", 
    "/affiliate.asp", "/affiliate.php", "/auth/", "/auth/login/", "/authorize.php", 
    "/autologin/", "/banneradmin/", "/base/admin/", "/bb-admin/", "/bbadmin/", 
    "/bb-admin/admin.asp", "/bb-admin/admin.html", "/bb-admin/admin.php", 
    "/bb-admin/index.asp", "/bb-admin/index.html", "/bb-admin/index.php", 
    "/bb-admin/login.asp", "/bb-admin/login.html", "/bb-admin/login.php", 
    "/bigadmin/", "/blogindex/", "/cadmins/", "/ccms/", "/ccms/index.php", 
    "/ccms/login.php", "/ccp14admin/", "/cms/", "/cms/admin/", "/cmsadmin/", 
    "/cms/_admin/logon.php", "/cms/login/", "/configuration/", "/configure/", 
    "/controlpanel/", "/controlpanel.asp", "/controlpanel.html", 
    "/controlpanel.php", "/cpanel/", "/cPanel/", "/cpanel_file/", "/cp.asp", 
    "/cp.html", "/cp.php", "/customer_login/", "/database_administration/", 
    "/Database_Administration/", "/db/admin.php", "/directadmin/", "/dir-login/", 
    "/editor/", "/edit.php", "/evmsadmin/", "/ezsqliteadmin/", "/fileadmin/", 
    "/fileadmin.asp", "/fileadmin.html", "/fileadmin.php", "/formslogin/", 
    "/forum/admin", "/globes_admin/", "/home.asp", "/home.html", "/home.php", 
    "/hpwebjetadmin/", "/include/admin.php", "/includes/login.php", "/Indy_admin/", 
    "/instadmin/", "/interactive/admin.php", "/irc-macadmin/", "/links/login.php", 
    "/LiveUser_Admin/", "/login/", "/login1/", "/login.asp", "/login_db/", 
    "/loginflat/", "/login.html", "/login/login.php", "/login.php", 
    "/login-redirect/", "/logins/", "/login-us/", "/logon/", "/logo_sysadmin/", 
    "/Lotus_Domino_Admin/", "/macadmin/", "/mag/admin/", "/maintenance/", 
    "/manage_admin.php", "/manager/", "/manager/ispmgr/", "/manuallogin/", 
    "/memberadmin/", "/memberadmin.asp", "/memberadmin.php", "/members/", 
    "/memlogin/", "/meta_login/", "/modelsearch/admin.asp", 
    "/modelsearch/admin.html", "/modelsearch/admin.php", "/modelsearch/index.asp", 
    "/modelsearch/index.html", "/modelsearch/index.php", "/modelsearch/login.asp", 
    "/modelsearch/login.html", "/modelsearch/login.php", "/moderator/", 
    "/moderator/admin.asp", "/moderator/admin.html", "/moderator/admin.php", 
    "/moderator.asp", "/moderator.html", "/moderator/login.asp", 
    "/moderator/login.html", "/moderator/login.php", "/moderator.php", 
    "/moderator.php/", "/myadmin/", "/navSiteAdmin/", "/newsadmin/", 
    "/nsw/admin/login.php", "/openvpnadmin/", "/pages/admin/admin-login.asp", 
    "/pages/admin/admin-login.html", "/pages/admin/admin-login.php", "/panel/", 
    "/panel-administracion/", "/panel-administracion/admin.asp", 
    "/panel-administracion/admin.html", "/panel-administracion/admin.php", 
    "/panel-administracion/index.asp", "/panel-administracion/index.html", 
    "/panel-administracion/index.php", "/panel-administracion/login.asp", 
    "/panel-administracion/login.html", "/panel-administracion/login.php", 
    "/panelc/", "/paneldecontrol/", "/panel.php", "/pgadmin/", "/phpldapadmin/", 
    "/phpmyadmin/", "/phppgadmin/", "/phpSQLiteAdmin/", "/platz_login/", "/pma/", 
    "/power_user/", "/project-admins/", "/pureadmin/", "/radmind/", "/radmind-1/", 
    "/rcjakar/admin/login.php", "/rcLogin/", "/server/", "/Server/", 
    "/ServerAdministrator/", "/server_admin_small/", "/Server.asp", 
    "/Server.html", "/Server.php", "/showlogin/", "/simpleLogin/", "/site/admin/", 
    "/siteadmin/", "/siteadmin/index.asp", "/siteadmin/index.php", 
    "/siteadmin/login.asp", "/siteadmin/login.html", "/site_admin/login.php", 
    "/siteadmin/login.php", "/smblogin/", "/sql-admin/", "/sshadmin/", 
    "/ss_vms_admin_sm/", "/staradmin/", "/sub-login/", "/Super-Admin/", 
    "/support_login/", "/sys-admin/", "/sysadmin/", "/SysAdmin/", "/SysAdmin2/", 
    "/sysadmin.asp", "/sysadmin.html", "/sysadmin.php", "/sysadmins/", 
    "/system_administration/", "/system-administration/", "/typo3/", "/ur-admin/", 
    "/ur-admin.asp", "/ur-admin.html", "/ur-admin.php", "/useradmin/", "/user.asp", 
    "/user.html", "/UserLogin/", "/user.php", "/usuario/", "/usuarios/", 
    "/usuarios//", "/usuarios/login.php", "/utility_login/", "/vadmind/", 
    "/vmailadmin/", "/webadmin/", "/WebAdmin/", "/webadmin/admin.asp", 
    "/webadmin/admin.html", "/webadmin/admin.php", "/webadmin.asp", 
    "/webadmin.html", "/webadmin/index.asp", "/webadmin/index.html", 
    "/webadmin/index.php", "/webadmin/login.asp", "/webadmin/login.html", 
    "/webadmin/login.php", "/webadmin.php", "/webmaster/", "/websvn/", 
    "/wizmysqladmin/", "/wp-admin/", "/wp-login/", "/wplogin/", "/wp-login.php", 
    "/xlogin/", "/yonetici.asp", "/yonetici.html", "/yonetici.php", 
    "/yonetim.asp", "/yonetim.html", "/yonetim.php", "/adm/", "/admin/", 
    "/admin/account.html", "/admin/login.html", "/admin/login.htm", 
    "/admin/controlpanel.html", "/admin/controlpanel.htm", "/admin/adminLogin.html", 
    "/admin/adminLogin.htm", "/admin.htm", "/admin.html", "/adminitem/", 
    "/adminitems/", "/administrator/", "/administrator/login.%EXT%", 
    "/administrator.%EXT%", "/administration/", "/administration.%EXT%", 
    "/adminLogin/", "/adminlogin.%EXT%", "/admin_area/admin.%EXT%", "/admin_area/", 
    "/admin_area/login.%EXT%", "/manager/", "/superuser/", "/superuser.%EXT%", 
    "/access/", "/access.%EXT%", "/sysadm/", "/sysadm.%EXT%", "/superman/", 
    "/supervisor/", "/panel.%EXT%", "/control/", "/control.%EXT%", "/member/", 
    "/member.%EXT%", "/members/", "/user/", "/user.%EXT%", "/cp/", "/uvpanel/", 
    "/manage/", "/manage.%EXT%", "/management/", "/management.%EXT%", "/signin/", 
    "/signin.%EXT%", "/log-in/", "/log-in.%EXT%", "/log_in/", "/log_in.%EXT%", 
    "/sign_in/", "/sign_in.%EXT%", "/sign-in/", "/sign-in.%EXT%", "/users/", 
    "/users.%EXT%", "/accounts/", "/accounts.%EXT%", "/bb-admin/login.%EXT%", 
    "/bb-admin/admin.%EXT%", "/bb-admin/admin.html", "/administrator/account.%EXT%", 
    "/relogin.htm", "/relogin.html", "/check.%EXT%", "/relogin.%EXT%", 
    "/blog/wp-login.%EXT%", "/user/admin.%EXT%", "/users/admin.%EXT%", 
    "/registration/", "/processlogin.%EXT%", "/checklogin.%EXT%", 
    "/checkuser.%EXT%", "/checkadmin.%EXT%", "/isadmin.%EXT%", 
    "/authenticate.%EXT%", "/authentication.%EXT%", "/auth.%EXT%", 
    "/authuser.%EXT%", "/authadmin.%EXT%", "/cp.%EXT%", "/modelsearch/login.%EXT%", 
    "/moderator.%EXT%", "/moderator/", "/controlpanel/", "/controlpanel.%EXT%", 
    "/admincontrol.%EXT%", "/adminpanel.%EXT%", "/fileadmin/", "/fileadmin.%EXT%", 
    "/sysadmin.%EXT%", "/admin1.%EXT%", "/admin1.html", "/admin1.htm", 
    "/admin2.%EXT%", "/admin2.html", "/yonetim.%EXT%", "/yonetim.html", 
    "/yonetici.%EXT%", "/yonetici.html", "/phpmyadmin/", "/myadmin/", 
    "/ur-admin.%EXT%", "/ur-admin/", "/Server.%EXT%", "/Server/", "/wp-admin/", 
    "/administr8.%EXT%", "/administr8/", "/webadmin/", "/webadmin.%EXT%", 
    "/administratie/", "/admins/", "/admins.%EXT%", "/administrivia/", 
    "/Database_Administration/", "/useradmin/", "/sysadmins/", "/sysadmins/", 
    "/admin1/", "/system-administration/", "/administrators/", "/pgadmin/", 
    "/directadmin/", "/staradmin/", "/ServerAdministrator/", "/SysAdmin/", 
    "/administer/", "/LiveUser_Admin/", "/sys-admin/", "/typo3/", "/panel/", 
    "/cpanel/", "/cpanel_file/", "/platz_login/", "/rcLogin/", "/blogindex/", 
    "/formslogin/", "/autologin/", "/manuallogin/", "/simpleLogin/", 
    "/loginflat/", "/utility_login/", "/showlogin/", "/memlogin/", 
    "/login-redirect/", "/sub-login/", "/wp-login/", "/login1/", "/dir-login/", 
    "/login_db/", "/xlogin/", "/smblogin/", "/customer_login/", "/UserLogin/", 
    "/login-us/", "/acct_login/", "/bigadmin/", "/project-admins/", "/phppgadmin/", 
    "/pureadmin/", "/sql-admin/", "/radmind/", "/openvpnadmin/", "/wizmysqladmin/", 
    "/vadmind/", "/ezsqliteadmin/", "/hpwebjetadmin/", "/newsadmin/", "/adminpro/", 
    "/Lotus_Domino_Admin/", "/bbadmin/", "/vmailadmin/", "/Indy_admin/", 
    "/ccp14admin/", "/irc-macadmin/", "/banneradmin/", "/sshadmin/", 
    "/phpldapadmin/", "/macadmin/", "/administratoraccounts/", "/admin4_account/", 
    "/admin4_colon/", "/radmind-1/", "/Super-Admin/", "/AdminTools/", "/cmsadmin/", 
    "/SysAdmin2/", "/globes_admin/", "/cadmins/", "/phpSQLiteAdmin/", 
    "/navSiteAdmin/", "/server_admin_small/", "/logo_sysadmin/", "/power_user/", 
    "/system_administration/", "/ss_vms_admin_sm/", "/bb-admin/", 
    "/panel-administracion/", "/instadmin/", "/memberadmin/", 
    "/administratorlogin/", "/adm.%EXT%", "/admin_login.%EXT%", 
    "/panel-administracion/login.%EXT%", "/pages/admin/admin-login.%EXT%", 
    "/pages/admin/", "/acceso.%EXT%", "/admincp/login.%EXT%", "/admincp/", 
    "/adminarea/", "/admincontrol/", "/affiliate.%EXT%", "/adm_auth.%EXT%", 
    "/memberadmin.%EXT%", "/administratorlogin.%EXT%", "/modules/admin/", 
    "/administrators.%EXT%", "/siteadmin/", "/siteadmin.%EXT%", "/adminsite/", 
    "/kpanel/", "/vorod/", "/vorod.%EXT%", "/vorud/", "/vorud.%EXT%", 
    "/adminpanel/", "/PSUser/", "/secure/", "/webmaster/", "/webmaster.%EXT%", 
    "/autologin.%EXT%", "/userlogin.%EXT%", "/admin_area.%EXT%", "/cmsadmin.%EXT%", 
    "/security/", "/usr/", "/root/", "/secret/", "/admin/login.%EXT%", 
    "/admin/adminLogin.%EXT%", "/moderator.php", "/moderator.html", 
    "/moderator/login.%EXT%", "/moderator/admin.%EXT%", "/yonetici.%EXT%", 
    "/0admin/", "/0manager/", "/aadmin/", "/cgi-bin/login%EXT%", "/login1%EXT%", 
    "/login_admin/", "/login_admin%EXT%", "/login_out/", "/login_out%EXT%", 
    "/login_user%EXT%", "/loginerror/", "/loginok/", "/loginsave/", 
    "/loginsuper/", "/loginsuper%EXT%", "/login%EXT%", "/logout/", 
    "/logout%EXT%", "/secrets/", "/super1/", "/super1%EXT%", "/super_index%EXT%", 
    "/super_login%EXT%", "/supermanager%EXT%", "/superman%EXT%", 
    "/superuser%EXT%", "/supervise/", "/supervise/Login%EXT%", "/super%EXT%"
]

# Handle %EXT% by replacing with common extensions
EXTENSIONS = [".php", ".asp", ".html", ".htm", ""]
EXPANDED_ADMIN_URLS = []
for url in ADMIN_URLS:
    if "%EXT%" in url:
        for ext in EXTENSIONS:
            EXPANDED_ADMIN_URLS.append(url.replace("%EXT%", ext))
    else:
        EXPANDED_ADMIN_URLS.append(url)

# Remove duplicates and sort
ADMIN_URLS = sorted(list(set(EXPANDED_ADMIN_URLS)))

# Queue to hold URLs for multithreading
url_queue = Queue()
results = []

def banner():
    print(Fore.CYAN + """
    ==============================
       Admin Panel Finder v2.0
       For Ethical Testing Only
       By Grok (Educational Tool)
    ==============================
    """)

def check_url(base_url, path):
    """Check if a URL exists and analyze the response."""
    full_url = urljoin(base_url, path)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(full_url, headers=headers, timeout=5, allow_redirects=True)
        status_code = response.status_code
        content = response.text.lower()

        # Detect potential login pages
        is_login_page = any(keyword in content for keyword in [
            "login", "username", "password", "admin", "sign in", "sign-in"
        ])

        if status_code == 200:
            if is_login_page:
                result = f"{Fore.GREEN}[+] Found potential login page: {full_url} (Status: {status_code}){Fore.RESET}"
            else:
                result = f"{Fore.YELLOW}[+] Found: {full_url} (Status: {status_code}){Fore.RESET}"
        elif status_code in [301, 302]:
            result = f"{Fore.BLUE}[*] Redirect: {full_url} (Status: {status_code}) to {response.headers.get('Location', 'unknown')}{Fore.RESET}"
        elif status_code == 403:
            result = f"{Fore.RED}[-] Forbidden: {full_url} (Status: {status_code}){Fore.RESET}"
        else:
            result = None

        if result:
            print(result)
            results.append(result)

    except requests.RequestException as e:
        print(f"{Fore.RED}[-] Error checking {full_url}: {e}{Fore.RESET}")

def worker(base_url):
    """Worker thread to process URLs from the queue."""
    while not url_queue.empty():
        path = url_queue.get()
        check_url(base_url, path)
        url_queue.task_done()

def scan_admin_panels(base_url, threads=10):
    """Scan the website for admin panel URLs using multiple threads."""
    print(f"[*] Scanning {base_url} with {threads} threads...")
    print(f"[*] Checking {len(ADMIN_URLS)} URLs...")
    start_time = time.time()

    # Populate the queue with URLs
    for path in ADMIN_URLS:
        url_queue.put(path)

    # Start worker threads
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(base_url,))
        t.daemon = True
        t.start()
        thread_list.append(t)

    # Wait for all threads to complete
    url_queue.join()

    # Save results to a file
    output_file = "admin_scan_results.txt"
    with open(output_file, "w") as f:
        for result in results:
            f.write(result + "\n")
    print(f"\n[*] Results saved to {output_file}")

    elapsed_time = time.time() - start_time
    print(f"[*] Scan completed in {elapsed_time:.2f} seconds.")

def main():
    parser = argparse.ArgumentParser(description="Admin Panel Finder for Ethical Testing")
    parser.add_argument("url", help="Target website URL (e.g., http://crestvtu.com)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    args = parser.parse_args()

    base_url = args.url
    if not base_url.startswith(("http://", "https://")):
        base_url = "http://" + base_url

    banner()
    scan_admin_panels(base_url, args.threads)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Scan interrupted by user. Exiting...")
        sys.exit(0)