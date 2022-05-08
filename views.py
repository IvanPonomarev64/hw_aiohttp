import bcrypt
import gino
from aiohttp import web

from db.tables import Owner, Advertisement, Token
from exception import HTTPError
from validation import validator_model, OwnerModel, AdvertisementModel


class OwnerView(web.View):
    async def post(self):
        json_data = validator_model((await self.request.json()), OwnerModel)
        new_entry = Owner(email=json_data['email'],
                          password=bcrypt.hashpw(json_data['password'].encode(), bcrypt.gensalt()).decode())
        try:
            await new_entry.create()
            return web.json_response(new_entry.to_dict())
        except Exception as ex:
            print(ex)

    async def get(self):
        json_data = validator_model((await self.request.json()), OwnerModel)
        owner = await Owner.query.where(Owner.email == json_data['email']).gino.first()
        return web.json_response(
            {'id': owner.id,
             "email": owner.email}
        )


class AdvertisementView(web.View):
    async def post(self):
        json_data = validator_model((await self.request.json()), AdvertisementModel)
        token = await Token.query.where(Token.id == json_data['token']).gino.first()
        if token:
            try:
                new_entry = await Advertisement.create(title=json_data['title'],
                                                       description=json_data['description'],
                                                       owner_id=token.owner_id)
                return web.json_response(new_entry.to_dict())
            except web.HTTPError as ex:
                print(ex)
        raise HTTPError(401, "you are not logged in")

    async def get(self):
        json_data = await self.request.json()
        adv = await Advertisement.query.where(Advertisement.title == json_data['title']).gino.first()
        if adv:
            return web.json_response(
                adv.to_dict()
            )
        raise HTTPError(404, "Advertisement not found")

    async def delete(self):
        json_data = await self.request.json()
        token = await Token.query.where(Token.id == json_data['token']).gino.first()
        adv = await Advertisement.query.where(Advertisement.title == json_data['title']).gino.first()
        if token:
            if token.owner_id == adv.owner_id:
                try:
                    await adv.delete()
                    return web.json_response({'status': 'ok'})
                except gino.exceptions.GinoException as ex:
                    print(ex)
            raise HTTPError(400, 'Запись может удалять только владелец')
        raise HTTPError(401, "you are not logged in")


async def login(request):
    json_data = await request.json()
    owner = await Owner.query.where(Owner.email == json_data['email']).gino.first()
    check_password = bcrypt.checkpw(json_data['password'].encode(), owner.password.encode())
    if not owner:
        raise HTTPError(401, "invalid login")

    elif not check_password:
        raise HTTPError(401, "invalid password")

    elif owner and check_password:
        token = await Token.create(owner_id=owner.id)
        return web.json_response({'token': f"{token.id}"})  # content_type='application/json'
