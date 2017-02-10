import unittest
import utils


class TestSuite(unittest.TestCase):

    name = "Oscar"
    email = "oscarchang1226@gmail.com"
    fake_email = "changtun@example.com"
    p = "changtun"
    salt = utils.generateRandomString()
    hash = utils.generateHash(p, salt)
    user = None

    def TestUserFunction(self):
        self.assertEqual(utils.getAllUsers().count(), 0)
        
        self.user = utils.createUser(
            name=self.name, email=self.email,
            salt=self.salt, hash=self.hash
        )
        self.assertIsNotNone(self.user)

        self.assertIs(utils.getUserByEmail(self.email).id, self.user.id)
        self.assertIsNone(utils.getUserByEmail(self.fake_email))

        salt = utils.generateRandomString()

        self.assertIsNone(utils.createUser(
            name="Tun", email=self.email,
            salt=salt,
            hash=utils.generateHash("testing", salt)
        ))


if __name__ == "__main__":
    unittest.main()
