import unittest
import utils


class TestSuite(unittest.TestCase):

    name = "Chang"
    email = "chang@example.com"
    salt = utils.generateRandomString()
    hash = utils.generateHash("chang", salt)

    def testA(self):
        name = "Oscar"
        email = "oscarchang1226@example.com"
        fake_email = "changtun@example.com"
        p = "changtun"
        salt = utils.generateRandomString()
        hash = utils.generateHash(p, salt)
        user = utils.createUser(
            name=name, email=email,
            salt=salt, hash=hash
        )
        # Test if user is created.
        self.assertIsNotNone(user)

        # Test getting user by email
        self.assertEquals(utils.getUserByEmail(email).id, user.id)
        self.assertIsNone(utils.getUserByEmail(fake_email))

        # Test getting user by id
        self.assertEquals(utils.getUserById(user.id).id, user.id)

        # Test delete user
        utils.deleteUser(user.id)
        user = utils.getUserById(user.id)
        self.assertIsNone(user)

    def testB(self):

        user = utils.createUser(
            name=self.name, email=self.email,
            salt=self.salt, hash=self.hash
        )

        # Test create a category
        category = utils.createCategory(
            name="FruitsTest",
            description="the sweet and fleshy product of a tree or other plant that contains seed and can be eaten as food.",  # NOQA
            user_id=user.id
        )
        self.assertIsNotNone(category)

        # Test get categories by user id
        test_categories = [
            "ChineseTest", "KoreanTest", "JapanseseTest", "FilipinoTest"
        ]
        for test in test_categories:
            utils.createCategory(name=test, description=test, user_id=user.id)

        self.assertEquals(len(utils.getCategoriesByUserId(user.id)), 5)

        # Test get all categories
        self.assertGreaterEqual(
            len(utils.getCategories()),
            len(utils.getCategoriesByUserId(user.id))
        )

        category_id = category.id

        # Test edit a category
        category = utils.editCategory(
            category_id, name="FoodTest", description="Delicious"
        )
        self.assertIsNotNone(category)
        self.assertEquals(category.description, "Delicious")

        # Test delete a category
        utils.deleteCategory(category_id)
        self.assertIsNone(utils.getCategoryById(category_id))

        for category in utils.getCategoriesByUserId(user.id):
            utils.deleteCategory(category.id)

        utils.deleteUser(user.id)

    def testC(self):

        user = utils.createUser(
            name=self.name, email=self.email,
            salt=self.salt, hash=self.hash
        )

        test_categories = [
            "ChineseTest", "KoreanTest", "JapanseseTest", "FilipinoTest"
        ]
        for test in test_categories:
            utils.createCategory(name=test, description=test, user_id=user.id)

        test_items = [
            "Item1", "Item2", "Item3", "Item4"
        ]

        # Test create items
        for category in utils.getCategoriesByUserId(user.id):
            for item in test_items:
                utils.createItem(
                    name=item, user_id=user.id, category_id=category.id
                )

        # Test get items by category id
        for category in utils.getCategoriesByUserId(user.id):
            self.assertEquals(
                len(utils.getItemsByCategoryId(category.id)), 4
            )

        # Test edit items
        for item in utils.getItemsByUserId(user.id):
            utils.editItem(item.id, description="IGNORE THIS TEST ITEM")

        for item in utils.getItemsByUserId(user.id):
            self.assertEquals(item.description, "IGNORE THIS TEST ITEM")

        # Test get items
        self.assertGreaterEqual(len(utils.getItems(12)), 12)

        # Test delete items
        for item in utils.getItemsByUserId(user.id):
            utils.deleteItem(item.id)
        self.assertFalse(list(utils.getItemsByUserId(user.id)))

        for category in utils.getCategoriesByUserId(user.id):
            utils.deleteCategory(category.id)

        utils.deleteUser(user.id)


if __name__ == "__main__":
    unittest.main(
        failfast=True, verbosity=2
    )
