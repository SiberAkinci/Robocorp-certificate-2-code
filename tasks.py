from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
pdf = PDF()
"""aaaa"""
archive = Archive()
@task
def order_robots_from_rsb():
    open_robot_order_website()
    close_annoying_modal()
    get_orders()
    archive_receipts()
    print(".")
def fill_the_form(orders):
    page= browser.page()
    head_names = {
        "1" : "Roll-a-thor head",
        "2" : "Peanut crusher head",
        "3" : "D.A.V.E head",
        "4" : "Andy Roid head",
        "5" : "Spanner mate head",
        "6" : "Drillbit 2000 head"
    }
    head_number = orders["Head"]
    page.select_option("#head",head_names[head_number])
    page.click('//*[@id="root"]/div/div[1]/div/div[1]/form/div[2]/div/div[{0}]/label'.format(orders["Body"]))
    page.fill("input[placeholder='Enter the part number for the legs']", orders["Legs"])
    page.fill("#address",orders["Address"])
    page.click("#order")
    while True:
        oa_checker = page.query_selector("#order-another")
        o_checker = page.query_selector("#order")
        if oa_checker:
            pdf_path=store_receipt_as_pdf(int(orders["Order number"]))
            ss_path=screenshot_robot(int(orders["Order number"]))
            embed_screenshot_to_pdf(ss_path,pdf_path)
            page.click("#order-another")
            close_annoying_modal()
            break
        elif o_checker:
            page.click("#order")
            


def close_annoying_modal():
    page = browser.page()
    page.click('text=OK')
def open_robot_order_website():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def get_orders():
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv",overwrite=True)
    table = Tables()
    orders = table.read_table_from_csv("orders.csv",columns=["Order number","Head","Body","Legs","Address"])
    for order in orders:
        fill_the_form(order)

def store_receipt_as_pdf(order_number):
    page = browser.page()
    receipt_html = page.locator("#receipt").inner_html()
    pdf_file_path = f"output/receipts/{order_number}.pdf"
    pdf.html_to_pdf(receipt_html, pdf_file_path)
    return pdf_file_path
def screenshot_robot(order_number):
    page = browser.page()
    screenshot_path = "output/screenshots/{0}.png".format(order_number)
    page.locator("#robot-preview-image").screenshot(path=screenshot_path)
    return screenshot_path
def embed_screenshot_to_pdf(screenshot_path,pdf_path):
    pdf.add_watermark_image_to_pdf(image_path=screenshot_path, 
                                   source_path=pdf_path, 
                                   output_path=pdf_path)
def archive_receipts():
    archive.archive_folder_with_zip("output/receipts", "output/receipts.zip")