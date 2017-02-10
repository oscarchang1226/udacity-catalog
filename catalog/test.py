import unittest
import utils


class TestSuite(unittest.TestCase):

    name = "Chang"
    email = "chang@example.com"
    salt = utils.generateRandomString()
    hash = utils.generateHash("chang", salt)
    user = None

    @classmethod
    def tearDownClass(self):
        # Delete categories assign by user
        for category in utils.getCategoriesByUserId(self.user.id):
            utils.deleteCategory(category)

        # Delete assigned user
        utils.deleteUser(self.user.id)

    def testUserFunction(self):
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

        # Asign a user for test
        self.user = utils.createUser(
            name=self.name, email=self.email,
            salt=self.salt, hash=self.hash
        )

    def testCategoryFunction(self):

        # Test create a category
        category = utils.createCategory(
            name="FruitsTest",
            description="the sweet and fleshy product of a tree or other plant that contains seed and can be eaten as food.",  # NOQA
            user=self.user
        )
        self.assertIsNotNone(category)

        # Test get categories by user id
        test_categories = [
            "ChineseTest", "KoreanTest", "JapanseseTest", "FilipinoTest"
        ]
        for test in test_categories:
            utils.createCategory(name=test, description=test)

        self.assertEquals(len(utils.getCategoriesByUserId(self.user.id)), 5)

        # Test get all categories
        self.assertGreaterEqual(
            len(utils.getCategories()),
            len(utils.getCategoriesByUserId(self.user.id))
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

    def testItemFunction(self):
        test_items = [
            "Item1", "Item2", "Item3", "Item4"
        ]

        # Test create items
        for category in utils.getCategoriesByUserId(self.user.id):
            for item in test_items:
                utils.createItem(
                    name=item, user=self.user, category=category
                )

        # Test get items by category id
        for category in utils.getCategoriesByUserId(self.user.id):
            self.assertEquals(
                len(utils.getItemsByCategoryId(category.id)), 4
            )

        # Test edit items
        for item in utils.getItemsByUserId(self.user.id):
            utils.editItem(item.id, description="IGNORE THIS TEST ITEM")

        for item in utils.getItemsByUserId(self.user.id):
            self.assertEquals(item.description, "IGNORE THIS TEST ITEM")

        # Test delete items
        for item in utils.getItemsByUserId(self.user.id):
            utils.deleteItem(item)
        self.assertFalse(list(utils.getItemsByUserId(self.user.id)))


if __name__ == "__main__":
    unittest.main(
        failfast=True, verbosity=2
    )
