from db.tables import web
from views import OwnerView, AdvertisementView, login


urls = [
    web.post('/owners/', OwnerView),
    web.get('/get-owners/', OwnerView),
    web.post('/post-adv/', AdvertisementView),
    web.get('/get-adv/', AdvertisementView),
    web.delete('/delete-adv/', AdvertisementView),
    web.post('/login/', login)
]

