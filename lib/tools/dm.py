import os
from lib.tools.colors import wh, r, g, y
from lib.tools.utils import clear, banner

def clean():
    lines_seen = set()
    with open('Result/dorkstest.txt', "r") as infile, open('Result/dorks.txt', "w") as outfile:
        for line in infile:
            if line not in lines_seen:
                outfile.write(line)
                lines_seen.add(line)
    os.remove('Result/dorkstest.txt')
    print(f"\n{wh}[{g}~{wh}] Duplicate dorks removed successfully!")
    print(f"\n{wh}[{g}+{wh}] Dorks saved as {g}Result/dorks.txt{y}!")

def dork():
    clear()
    print(banner + f"\n{wh}[{g}!{wh}] Using Tools Dork Maker")
    text = input(f"\n{wh}[{g}+{wh}] Please input any text : ")
    words = text.split()
    print(f"{wh}[{g}!{wh}] {len(words)} text verified! Now let's make some dorks!\n")
    print(f"\n{wh}[{g}1{wh}] WordPress")
    print(f"{wh}[{g}2{wh}] Joomla")
    print(f"{wh}[{g}3{wh}] OpenCart")
    
    cms = input(f"\n{wh}[{g}?{wh}] Which CMS dorks do you want to make? : ")
    
    dorks_dict = {
        "1": {"WordPress": [
            "(\"Comment on Hello world!\") ",
            "(\"author/admin\")",
            "(\"uncategorized/hello-world\") ",
            "(\"Proudly powered by WordPress\") ",
            "(\"Welcome to WordPress. This is your first post.\") ",
            "(\"wp-content/plugins/\")",
            "(\"wp-content/themes/\")",
            "(\"wp-login.php\")",
            "(\"inurl:wp-content/uploads\")",
            "(\"inurl:wp-json/wp/v2/\")",
            "(\"inurl:wp-admin/admin-ajax.php\")",
            "(\"wp-content/cache\")",
            "(\"wp-includes/js/jquery/\")",
            "(\"wp-content/languages\")",
            "(\"wp-content/debug.log\")",
            "(\"wp-includes/css/\")",
            "(\"wp-admin/css/\")",
            "(\"wp-config.php.bak\")",
            "(\"wp-content/uploads/backup\")",
            "(\"inurl:wp-admin/setup-config.php\")"
        ]},
        "2": {"Joomla": [
            "index.php?option=com_users ",
            "index.php?option=com_jce ",
            "(\"com_user\")",
            "(\"index.php?option=com_content\")",
            "(\"index.php?option=com_k2\")",
            "(\"index.php?option=com_weblinks\")",
            "(\"inurl:administrator/index.php\")",
            "(\"inurl:com_virtuemart\")",
            "(\"inurl:com_finder\")",
            "(\"index.php?option=com_contact\")",
            "(\"index.php?option=com_banners\")",
            "(\"index.php?option=com_newsfeeds\")",
            "(\"index.php?option=com_redirect\")",
            "(\"index.php?option=com_mailto\")",
            "(\"index.php?option=com_search\")",
            "(\"index.php?option=com_wrapper\")",
            "(\"index.php?option=com_poll\")",
            "(\"index.php?option=com_installer\")"
        ]},
        "3": {"OpenCart": [
            "index.php?route=product ",
            "index.php?route=",
            "(\"index.php?route=common/home\")",
            "(\"index.php?route=checkout/cart\")",
            "(\"index.php?route=account/login\")",
            "(\"index.php?route=product/product\")",
            "(\"index.php?route=information/contact\")",
            "(\"index.php?route=account/register\")",
            "(\"index.php?route=affiliate/account\")",
            "(\"index.php?route=product/category\")",
            "(\"index.php?route=account/password\")",
            "(\"index.php?route=account/address\")",
            "(\"index.php?route=account/wishlist\")",
            "(\"index.php?route=account/download\")",
            "(\"index.php?route=common/footer\")",
            "(\"index.php?route=checkout/guest\")",
            "(\"index.php?route=information/sitemap\")",
            "(\"index.php?route=account/return\")",
            "(\"index.php?route=product/manufacturer\")"
        ]}
    }
    
    if cms in dorks_dict:
        cms_name, cms_dorks = list(dorks_dict[cms].items())[0]
        print(f"[{r}+{y}] Prepared dorks for {cms_name}:\n")
        
        with open("Result/dorkstest.txt", "w") as f:
            for dork in cms_dorks:
                for word in words:
                    line = dork + word
                    print(line)
                    f.write(line + "\n")
        
        input(f"\n{wh}[{g}+{wh}] Press enter to remove duplicate dorks...")
        clean()
    else:
        print(f"{wh}[{r}!{wh}] Invalid Option! Tool closed!")

if __name__ == "__main__":
    dork()
