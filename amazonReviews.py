

# import time
# import random
# import pandas as pd
# import getpass
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import re  

# # Pide usuario y contraseña por terminal
# amazon_user =  input("Amazon usuario/email: ")
# amazon_pass =  getpass.getpass("Amazon contraseña: ")

# # Configuración de Selenium
# service = Service('/usr/local/bin/chromedriver')

# options = webdriver.ChromeOptions()
# # options.add_argument('--headless')  # puedes activar si quieres ocultar ventana
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0 Safari/537.36')

# driver = webdriver.Chrome(service=service, options=options)

# def do_login():
#     print('🔑 Realizando login...')
#     driver.get('https://www.amazon.com/-/es/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')
#     WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ap_email')))
#     driver.find_element(By.ID, 'ap_email').send_keys(amazon_user)
#     driver.find_element(By.ID, 'continue').click()
#     WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ap_password')))
#     driver.find_element(By.ID, 'ap_password').send_keys(amazon_pass)
#     driver.find_element(By.ID, 'signInSubmit').click()
#     time.sleep(5)

# def check_and_login_if_needed(current_url):
#     if '/ap/signin' in driver.current_url or 'ap_email' in driver.page_source:
#         print('🚨 Detectado redireccionamiento a login.')
#         do_login()
#         driver.get(current_url)
#         time.sleep(random.uniform(3, 6))

# try:
#     # Primer login manual
#     do_login()    # Ir a los más vendidos en tecnología
#     driver.get('https://www.amazon.com/-/es/gp/bestsellers/electronics')
#     time.sleep(random.uniform(3, 5))

#     # Extraer ASINs
#     product_links = driver.find_elements(By.CSS_SELECTOR, 'div.zg-grid-general-faceout a.a-link-normal')
#     asin_list = []
#     for link in product_links[:100]:
#         href = link.get_attribute('href')
#         if '/dp/' in href:
#             asin = href.split('/dp/')[1].split('/')[0]
#             if asin not in asin_list:
#                 asin_list.append(asin)

#     print(f'✅ Encontrados {len(asin_list)} productos únicos para scrapear.')

#     all_data = []

#     for asin in asin_list:
#         print(f'\nScrapeando reseñas para producto ASIN: {asin}')
#         for page in range(1, 11):  # hasta 10 páginas
#             review_url = f'https://www.amazon.com/product-reviews/{asin}/?pageNumber={page}'
#             driver.get(review_url)
#             time.sleep(random.uniform(3, 6))

#             check_and_login_if_needed(review_url)

#             reviews = driver.find_elements(By.CSS_SELECTOR, '[data-hook="review"]')
#             if not reviews:
#                 print(f'⚠️ No se encontraron reseñas en página {page}. Salto a siguiente producto.')
#                 break

#             for review in reviews:
#                 try:
#                     # check_and_login_if_needed(review_url)
#                     review_title = review.find_element(By.CSS_SELECTOR, '[data-hook="review-title"]').text.strip()
#                     raw_rating = review.find_element(By.CSS_SELECTOR, '[data-hook="review-star-rating"]').text.strip()
#                     raw_rating2 = review.find_element(By.CSS_SELECTOR, '[data-hook="review-star-rating-view-point"]').text.strip()
#                     print(f' Calificación: {raw_rating}')  # Confirmación visual
#                     print(f' Calificación: {raw_rating2}')  # Confirmación visual

#                     date = review.find_element(By.CSS_SELECTOR, '[data-hook="review-date"]').text.strip()
#                     body = review.find_element(By.CSS_SELECTOR, '[data-hook="review-body"]').text.strip()
#                     all_data.append({
#                         'asin': asin,
#                         'titulo_reseña': review_title,
#                         'calificacion': raw_rating2,  # numérico
#                         'fecha': date,
#                         'comentario': body
#                     })
#                     # rating = float(raw_rating.split(' ')[0]) if 'de' in raw_rating else None
                   
#                     # star_element = review.find_element(By.CSS_SELECTOR, 'span.a-icon-alt')
#                     # raw_rating = star_element.text.strip()  # Ej: "4.0 de 5 estrellas"
#                     # match = re.search(r'(\d+(\.\d+)?)', raw_rating)
#                     # rating = float(match.group(1)) if match else None
#                     #                   
#                     # try:
#                     #     star_element = review.find_element(By.CSS_SELECTOR, 'span.a-icon-alt')
#                     # except NoSuchElementException:
#                     #     try:
#                     #         star_element = review.find_element(By.CSS_SELECTOR, '[data-hook="review-star-rating-view-point"]')
#                     #     except NoSuchElementException:
#                     #         star_element = None

#                     # if star_element:
#                     #     raw_rating = star_element.text.strip()
#                     # else:
#                     #     raw_rating = ''

                    
                
#                 except NoSuchElementException as e:
#                     print(f'⚠️ Error al extraer reseña: {e}')
#                     continue

#     # Guardar CSV final
#     df = pd.DataFrame(all_data)
#     df.to_csv('reseñas_mas_vendidos_tecnologia.csv', index=False)
#     print(f'\n✅ Datos guardados en reseñas_mas_vendidos_tecnologia.csv ({len(df)} registros)')

# finally:
#     driver.quit()
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# import pandas as pd
# import time
# import random
# from textblob import TextBlob
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException


# # Configuración de Selenium
# service = Service('/usr/local/bin/chromedriver')  # Ajusta la ruta si es diferente
# options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0 Safari/537.36')
# driver = webdriver.Chrome(service=service, options=options)

# movie_data = []

# try:
#     driver.get('https://www.imdb.com/chart/top/')
#     time.sleep(5)

#     # Obtener bloques de las 10 películas más top
#     blocks = driver.find_elements(By.CSS_SELECTOR, 'ul.ipc-metadata-list > li')[:10]
#     print(f'🔍 Encontradas {len(blocks)} películas top para procesar.')
#     print(blocks)
    
#     for block in blocks:
#         # print(f'🔍 Procesando bloque: { block.text.strip()}')
        
#         try:
#             title_element = block.find_element(By.CSS_SELECTOR, 'h3.ipc-title__text')
#             title = title_element.text.strip()
#             link_element = block.find_element(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper')
#             href = link_element.get_attribute('href')
#             if not href.startswith('https://www.imdb.com'):
#                 href = 'https://www.imdb.com' + href
#         except Exception as e:
#             print(f'⚠️ Error extrayendo título y link: {e}')
#             continue

#         print(f'🎬 Procesando: {title}')
#         print(f'🎬 Procesando: {href}')
        
#         driver.get(href)
#         time.sleep(random.uniform(3, 5))

#         try:
#             genre = driver.find_element(By.CSS_SELECTOR, 'div.ipc-chip-list--baseAlt a.ipc-chip__text').text.strip()
#         except:
#             genre = 'N/A'
#         try:
#             duration = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="title-techspec_runtime"] span').text.strip()
#         except:
#             duration = 'N/A'
#         try:
#             release_date = driver.find_element(By.CSS_SELECTOR, 'a[href*="releaseinfo"]').text.strip()
#         except:
#             release_date = 'N/A'
#         try:
#             cast_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="title-cast-item__actor"]')[:3]
#             cast = ', '.join([actor.text.strip() for actor in cast_elements])
#         except:
#             cast = 'N/A'

#         # Scraping de reseñas
#         imdb_id = href.split('/')[5]
#         reviews_url = f'https://www.imdb.com/es/title/{imdb_id}/reviews/'
#         print(f'🔗 Accediendo a reseñas: {reviews_url}')
#         driver.get(reviews_url)
#         time.sleep(random.uniform(3, 5))
#         sections = driver.find_elements(By.CSS_SELECTOR, 'section.ipc-page-section.ipc-page-section--base.ipc-page-section--sp-pageMargin')
#         print(f'🔍 Encontradas {len(sections)} secciones de reseñas para procesar.')
#         for section in sections:
#             reviews = section.find_elements(By.CSS_SELECTOR, 'article.user-review-item')[:10]
#             print(f'🔍 Encontradas {len(reviews)} reseñas para procesar en esta sección.')
#             for review in reviews:
#                 try:
#                     rating_span = review.find_elements(By.CSS_SELECTOR, 'span.ipc-rating-star--rating')
#                     rating = rating_span[0].text.strip() if rating_span else 'N/A'

#                     date_elem = review.find_element(By.CSS_SELECTOR, 'ul.ipc-inline-list--show-dividers li.review-date')
#                     date = date_elem.text.strip()

#                     # content = review.find_element(By.CSS_SELECTOR, 'div.ipc-html-content-inner-div').text.strip()
#                     try:
#                         content_elem = review.find_element(By.CSS_SELECTOR, 'div.ipc-html-content-inner-div')
#                         content = content_elem.text.strip()
#                     except NoSuchElementException:
#                         content = "N/A"


#                     print(f'🎭 Reseña: {content[:50]}...')  # Muestra los primeros 50 caracteres
#                     sentiment = TextBlob(content).sentiment.polarity

#                     movie_data.append({
#                         'pelicula': title,
#                         'genero': genre,
#                         'duracion': duration,
#                         'fecha_estreno': release_date,
#                         'reparto_principal': cast,
#                         'calificacion': rating,
#                         'fecha_resena': date,
#                         'contenido_resena': content,
#                         'sentimiento': sentiment
#                     })
#                 except Exception as e:
#                     print(f'⚠️ Error en reseña: {e}')
#                     continue
# finally:
#     driver.quit()

# # Guardar en CSV
# df = pd.DataFrame(movie_data)
# df.to_csv('imdb_top10_peliculas_resenas.csv', index=False)
# print("✅ Datos guardados en 'imdb_top10_peliculas_resenas.csv'")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import random
from textblob import TextBlob
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Configuración de Selenium
service = Service('/usr/local/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0 Safari/537.36')
driver = webdriver.Chrome(service=service, options=options)

movie_data = []

try:
    driver.get('https://www.imdb.com/chart/top/')
    time.sleep(5)

    # 1️⃣ Paso: Extraer título y URL de las 10 películas
    blocks = driver.find_elements(By.CSS_SELECTOR, 'ul.ipc-metadata-list > li')[:100]
    print(f'🔍 Encontradas {len(blocks)} películas top para procesar.')

    movie_infos = []
    for block in blocks:
        try:
            title = block.find_element(By.CSS_SELECTOR, 'h3.ipc-title__text').text.strip()
            href = block.find_element(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper').get_attribute('href')
            if not href.startswith('https://www.imdb.com'):
                href = 'https://www.imdb.com' + href
            movie_infos.append((title, href))
        except Exception as e:
            print(f'⚠️ Error extrayendo título y link: {e}')
            continue

    # 2️⃣ Paso: Recorrer la lista de títulos y URLs
    for title, href in movie_infos:
        print(f'🎬 Procesando: {title}')
        print(f'🎬 Procesando: {href}')

        driver.get(href)
        time.sleep(random.uniform(3, 5))

        # Extraer género, duración, estreno, reparto
        try:
            genre = driver.find_element(By.CSS_SELECTOR, 'div.ipc-chip-list--baseAlt a.ipc-chip__text').text.strip()
        except:
            genre = 'N/A'
        try:
            duration = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="title-techspec_runtime"] span').text.strip()
        except:
            duration = 'N/A'
        try:
            release_date = driver.find_element(By.CSS_SELECTOR, 'a[href*="releaseinfo"]').text.strip()
        except:
            release_date = 'N/A'
        try:
            cast_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="title-cast-item__actor"]')[:3]
            cast = ', '.join([actor.text.strip() for actor in cast_elements])
        except:
            cast = 'N/A'

        # Acceder a la página de reseñas
        imdb_id = href.split('/')[5]
        reviews_url = f'https://www.imdb.com/es/title/{imdb_id}/reviews/'
        print(f'🔗 Accediendo a reseñas: {reviews_url}')
        driver.get(reviews_url)
        time.sleep(random.uniform(3, 5))

        sections = driver.find_elements(By.CSS_SELECTOR, 'section.ipc-page-section.ipc-page-section--base.ipc-page-section--sp-pageMargin')
        print(f'🔍 Encontradas {len(sections)} secciones de reseñas para procesar.')

        for section in sections:
            reviews = section.find_elements(By.CSS_SELECTOR, 'article.user-review-item')[:10]
            print(f'🔍 Encontradas {len(reviews)} reseñas para procesar en esta sección.')
            for review in reviews:
                try:
                    rating_span = review.find_elements(By.CSS_SELECTOR, 'span.ipc-rating-star--rating')
                    rating = rating_span[0].text.strip() if rating_span else 'N/A'

                    date_elem = review.find_element(By.CSS_SELECTOR, 'ul.ipc-inline-list--show-dividers li.review-date')
                    date = date_elem.text.strip()

                    # Acceder al contenido de la reseña
                    try:
                        content_elem = review.find_element(
                            By.CSS_SELECTOR,
                            'div.ipc-overflowText--base > div.ipc-overflowText--children > div.ipc-html-content--base > div.ipc-html-content-inner-div'
                        )
                        content = content_elem.text.strip()
                    except NoSuchElementException:
                        content = "N/A"

                    print(f'🎭 Reseña: {content[:50]}...')  # Muestra los primeros 50 caracteres
                    sentiment = TextBlob(content).sentiment.polarity

                    movie_data.append({
                        'pelicula': title,
                        'genero': genre,
                        'duracion': duration,
                        'fecha_estreno': release_date,
                        'reparto_principal': cast,
                        'calificacion': rating,
                        'fecha_resena': date,
                        'contenido_resena': content,
                        'sentimiento': sentiment
                    })
                except Exception as e:
                    print(f'⚠️ Error en reseña: {e}')
                    continue

finally:
    driver.quit()

# Guardar en CSV
df = pd.DataFrame(movie_data)
df.to_csv('imdb_top10_peliculas_resenas.csv', index=False)
print("✅ Datos guardados en 'imdb_top10_peliculas_resenas.csv'")
