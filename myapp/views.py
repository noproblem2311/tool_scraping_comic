from django.http import HttpResponse
from django.conf import settings
# from google.cloud import storage
import io
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# myapp/views.py
from django.shortcuts import render
from .forms import FilterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect

def nhapdata(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            min_rating = form.cleaned_data['min_rating']
            link = form.cleaned_data['link']

            # Store values in the session
            request.session['min_rating'] = min_rating
            request.session['link'] = link

            # Redirect to the timtruyen_selenium view
            return redirect('timtruyen_selenium')

    else:
        form = FilterForm()

    return render(request, 'nhapdata.html', {'form': form})
def timtruyen_selenium(request):
       # Retrieve values from the session
    min_rating = float(request.session.get('min_rating', 0.0))
    base_link = request.session.get('link', '')

  
    print("===============================",min_rating,"================================")
    print("===============================",base_link,"================================")
    tentruyen_html = ''
    driver = webdriver.Chrome()

    try:
        for i in range(1, 5):
            tentruyen = []
            driver.get(f'{base_link}&page={i}')
            
            try:
                jtip_links = driver.find_elements(By.CSS_SELECTOR, 'a.jtip')
            except Exception as e:
                print("Could not find elements on the page")
                continue

            main_window = driver.current_window_handle  # Save the main window handle
            
            for li in jtip_links:
                href_value = li.get_attribute('href')
                
                # Open the link in a new tab and handle exceptions
                try:
                    script = f"window.open('{href_value}', '_blank');"
                    driver.execute_script(script)
                    driver.switch_to.window(driver.window_handles[-1])
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[itemprop="ratingValue"]')))
                except Exception as e:
                    
                    continue

                try:
                    rating_elements = driver.find_elements(By.CSS_SELECTOR, 'span[itemprop="ratingValue"]')

                    for element in rating_elements:
                        rating_text = element.text
                        try:
                            rating_value = float(rating_text)
                        except ValueError:
                            rating_value = 0.0

                        if rating_value > min_rating:

                            title_element = driver.find_element(By.CSS_SELECTOR, 'h1.title-detail')
                            title_text = title_element.text
                            a = title_text + f'<a href="{href_value}"> link</a>' + f'{rating_text}'
                            tentruyen.append(a)
                except Exception as e:
                    print("Error in scraping data from details page")
                finally:
                    # Close the current tab and switch back to the main window
                    driver.close()
                    driver.switch_to.window(main_window)

            for truyen in tentruyen:
                tentruyen_html += truyen + '<br>'
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        driver.quit()

    return HttpResponse(tentruyen_html)