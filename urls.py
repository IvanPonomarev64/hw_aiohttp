from db.tables import app, web
from views import OwnerView, AdvertisementView, login

app.add_routes(
    [
        web.post('/owners/', OwnerView),
        web.get('/get-owners/', OwnerView),
        web.post('/post-adv/', AdvertisementView),
        web.get('/get-adv/', AdvertisementView),
        web.delete('/delete-adv/', AdvertisementView),
        web.post('/login/', login)

    ]
)
