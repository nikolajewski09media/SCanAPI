import os

def chosetherightwebmaster(location):
    try:
        os.rename(rf'{location}\\webmasters.dat',rf'{location}\\webmasters_sophia.dat')
        os.rename(rf'{location}\\webmasters_steffen.dat', rf'{location}\\webmasters.dat')
    except Exception:
        os.rename(rf'{location}\\webmasters.dat', rf'{location}\\webmasters_steffen.dat')
        os.rename(rf'{location}\\webmasters_sophia.dat', rf'{location}\\webmasters.dat')


def execute_request(service, domain, request):
  try:
      property_uri = f'https://{domain}/'
      return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()
  except Exception:
      property_uri = f'http://{domain}/'
      return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()
  
  
def startEndDialog():
    start_date = input('Btte geben Sie ein Startdatum ein (JJJJ-MM-TT): ')
    end_date = input('Btte geben Sie ein Enddatum ein (JJJJ-MM-TT): ')
    return start_date, end_date