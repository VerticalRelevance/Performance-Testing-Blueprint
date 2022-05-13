import time

from website.website_user import WebsiteUser


class UserJourney:
    def __init__(self, client):
        self._user = WebsiteUser(client)

    def browse_workflow(self):
        self._user.get_random_product()
        time.sleep(2)
        self._user.get_random_product()
        time.sleep(0.5)
        self._user.get_random_product()
        time.sleep(0.5)

    def abandon_cart(self):
        self._user.get_random_product()
        time.sleep(2)
        self._user.add_to_cart()
        time.sleep(1)
        self._user.get_random_product()
        time.sleep(0.5)
        self._user.add_to_cart()
        time.sleep(1)
        self._user.get_random_product()
        time.sleep(0.5)
        self._user.add_to_cart()

    def purchase_workflow(self):
        self._user.login_store()
        self._user.get_random_product()
        time.sleep(1)
        self._user.add_to_cart()
        time.sleep(0.5)
        self._user.view_cart()
        time.sleep(0.5)
        self._user.checkout()
        time.sleep(0.5)