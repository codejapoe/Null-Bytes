import uuid
import json
import re
import os.path
import pickle

# Store the data structure into a pickle file
def store_avl(structure):
    with open('database.pkl', 'wb') as f:
        pickle.dump(structure, f)


# Load the data structure from the pickle file
def load_avl():
    with open('database.pkl', 'rb') as f:
        return pickle.load(f)


# AVL Data Structure: Users -> Length (Length of User ID) -> ID -> User -> Database -> Sub_ID (Database ID) -> Data
class Users:
    def __init__(self, char, length, username, password, database, sub_str, sub_length, _id, data):
        self.char = char
        self.id = Length(length, username, password, database, sub_str, sub_length, _id, data)
        self.left = None
        self.right = None


class Length:
    def __init__(self, length, username, password, database, sub_str, sub_length, _id, data):
        self.length = length
        self.user_info = ID(username, password, database, sub_str, sub_length, _id, data)
        self.height = 1
        self.left = None
        self.right = None


class ID:
    def __init__(self, username, password, database, sub_str, sub_length, _id, data):
        self.username = username
        self.password = password
        self.user_data = User(database, sub_str, sub_length, _id, data)
        self.height = 1
        self.left = None
        self.right = None


class User:
    def __init__(self, database, sub_str, sub_length, _id, data):
        self.database = database
        self.data_id = Database(sub_str, sub_length, _id, data)
        self.height = 1
        self.left = None
        self.right = None


class Database:
    def __init__(self, sub_str, sub_length, _id, data):
        self.substr = sub_str
        self.sub_id = Sub_ID(sub_length, _id, data)
        self.left = None
        self.right = None


class Sub_ID:
    def __init__(self, sub_length, _id, data):
        self.sub_length = sub_length
        self.data_tree = Data(_id, data)
        self.height = 1
        self.left = None
        self.right = None


class Data:
    def __init__(self, _id, data):
        self._id = _id
        self.data = data
        self.height = 1
        self.left = None
        self.right = None


# Insert English alphabets and numbers into the Data Structure
def insertChar(root, char):
    if root is None:
        return Users(char, None, None, None, None, None, None, None, None)

    else:

        if char < root.char:
            root.left = insertChar(root.left, char)

        elif char > root.char:
            root.right = insertChar(root.right, char)

        return root


# Database setup
def startDatabase(root):
    char = ['i', '9', 'r', '4', 'e', 'n', 'w', '2', '7', 'c', 'g', 'l', 'p', 'u', 'y', '1', '3', '6', '8', 'b', 'd',
            'f', 'h', 'k', 'm', 'o', 'q', 't', 'v', 'x', 'z', '0', '5', 'a', 'j', 's']

    for i in char:
        root = insertChar(root, i)

    return root


# Database initalization
def insertCharintoDB(root, char):
    if root is None:
        return Database(char, None, None, None)

    else:

        if char < root.substr:
            root.left = insertCharintoDB(root.left, char)

        elif char > root.substr:
            root.right = insertCharintoDB(root.right, char)

        return root


# ID setup
def startID():
    root = None
    char = ['i', '9', 'r', '4', 'e', 'n', 'w', '2', '7', 'c', 'g', 'l', 'p', 'u', 'y', '1', '3', '6', '8', 'b', 'd',
            'f', 'h', 'k', 'm', 'o', 'q', 't', 'v', 'x', 'z', '0', '5', 'a', 'j', 's']

    for i in char:
        root = insertCharintoDB(root, i)

    return root


# Account creation
def createAccount(root, api):
    username = api['username']
    password = api['password']
    data = createAccount1(root, username, password)

    if data != False:
        root = data
        return root

    return data


def createAccount1(root, username, password):
    if username[0] == root.char:
        data = createAccount2(root.id, username, password)

        if data != False:
            root.id = data
            return root

    elif username[0] < root.char:
        data = createAccount1(root.left, username, password)

        if data != False:
            root.left = data
            return root

    elif username[0] > root.char:
        data = createAccount1(root.right, username, password)

        if data != False:
            root.right = data
            return root

    return data


def createAccount2(root, username, password):
    if root is None:
        return Length(len(username), username, password, None, None, None, None, None)

    else:

        if root.length is None:
            root.length = len(username)
            root.user_info.username = username
            root.user_info.password = password
            return root

        else:

            if len(username) == root.length:
                data = createAccount3(root.user_info, username, password)

                if data != False:
                    root.user_info = data
                    return root

            elif len(username) < root.length:
                data = createAccount2(root.left, username, password)

                if data != False:
                    root.left = data
                    return root

            elif len(username) > root.length:
                data = createAccount2(root.right, username, password)

                if data != False:
                    root.right = data
                    return root

            if data != False:
                root.height = 1 + max(getHeight(root.left), getHeight(root.right))

                balanceFactor = getBalance(root)

                if balanceFactor > 1:

                    if getBalance(root.left) >= 0:
                        return rightRotate(root)

                    else:
                        root.left = leftRotate(root)
                        return rightRotate(root)

                elif balanceFactor < -1:

                    if getBalance(root.right) <= 0:
                        return leftRotate(root)

                    else:
                        root.right = rightRotate(root.right)
                        return leftRotate(root)

                return root

            return data


def createAccount3(root, username, password):
    if root is None:
        return ID(username, password, None, None, None, None, None)

    else:

        if username < root.username:
            data = createAccount3(root.left, username, password)

            if data != False:
                root.left = data
                return root

        elif username > root.username:
            data = createAccount3(root.right, username, password)

            if data != False:
                root.right = data
                return root

        elif username == root.username:
            data = False

        return data


# Account deletion
def deleteAccount(root, api):
    username = api['username']
    password = api['password']

    if password == getUserInfo(root, username):
        root = deleteAccount1(root, username, password)

    return root


def deleteAccount1(root, username, password):
    if username[0] == root.char:
        root.id = deleteAccount2(root.id, username, password)

    elif username[0] < root.char:
        root.left = deleteAccount1(root.left, username, password)

    elif username[0] > root.char:
        root.right = deleteAccount1(root.right, username, password)

    return root


def deleteAccount2(root, username, password):
    if len(username) == root.length:
        root.user_info = deleteAccount3(root.user_info, username, password)

    elif len(username) < root.length:
        root.left = deleteAccount2(root.left, username, password)

    elif len(username) > root.length:
        root.right = deleteAccount2(root.right, username, password)

    root.height = 1 + max(getHeight(root.left), getHeight(root.right))

    balanceFactor = getBalance(root)

    if balanceFactor > 1:

        if getBalance(root.left) >= 0:
            return rightRotate(root)

        else:
            root.left = leftRotate(root)
            return rightRotate(root)

    elif balanceFactor < -1:

        if getBalance(root.right) <= 0:
            return leftRotate(root)

        else:
            root.right = rightRotate(root.right)
            return leftRotate(root)

    return root


def deleteAccount3(root, username, password):
    if username == root.username:
        if root.left is None:
            temp = root.right
            root = None
            return temp

        elif root.right is None:
            temp = root.left
            root = None
            return temp

        else:
            temp = getNode(root.right)
            root.username = temp.username
            root.password = temp.password
            root.user_data = temp.user_data
            root.right = deleteAccount3(root.right, temp.username)

    elif username < root.username:
        root.left = deleteAccount3(root.left, username, password)

    elif username > root.username:
        root.right = deleteAccount3(root.right, username, password)

    if root is not None:
        return root

    root.height = 1 + max(getHeight(root.left), getHeight(root.right))

    balanceFactor = getBalance(root)

    if balanceFactor > 1:

        if getBalance(root.left) >= 0:
            return rightRotate(root)

        else:
            root.left = leftRotate(root)
            return rightRotate(root)

    elif balanceFactor < -1:

        if getBalance(root.right) <= 0:
            return leftRotate(root)

        else:
            root.right = rightRotate(root.right)
            return leftRotate(root)

    return root


# Get user data
def getUserInfo(root, username):
    if username[0] == root.char:
        return getUserInfo2(root.id, username)

    elif username[0] < root.char:
        return getUserInfo(root.left, username)

    elif username[0] > root.char:
        return getUserInfo(root.right, username)


def getUserInfo2(root, username):
    if len(username) == root.length:
        return getUserInfo3(root.user_info, username)

    elif len(username) < root.length:
        return getUserInfo2(root.left, username)

    elif len(username) > root.length:
        return getUserInfo2(root.right, username)


def getUserInfo3(root, username):
    if username == root.username:
        return root.password

    elif username < root.username:
        return getUserInfo3(root.left, username)

    elif username > root.username:
        return getUserInfo3(root.right, username)


# Database creation
def createDatabase(root, api):
    username = api['username']
    database_id = api['database-id']

    data = createDatabase1(root, username, database_id)

    if data != False:
        root = data
        return root

    return data


def createDatabase1(root, username, _id):
    if username[0] == root.char:
        data = createDatabase2(root.id, username, _id)

        if data != False:
            root.id = data
            return root

    elif username[0] < root.char:
        data = createDatabase1(root.left, username, _id)

        if data != False:
            root.left = data
            return root

    elif username[0] > root.char:
        data = createDatabase1(root.right, username, _id)

        if data != False:
            root.right = data
            return root

    return data


def createDatabase2(root, username, _id):
    if len(username) == root.length:
        data = createDatabase3(root.user_info, username, _id)

        if data != False:
            root.user_info = data
            return root

    elif len(username) < root.length:
        data = createDatabase2(root.left, username, _id)

        if data != False:
            root.left = data
            return root

    elif len(username) > root.length:
        data = createDatabase2(root.right, username, _id)

        if data != False:
            root.right = data
            return root

    return data


def createDatabase3(root, username, _id):
    if username == root.username:
        data = createDatabase4(root.user_data, _id)

        if data != False:
            root.user_data = data
            if root.user_data.data_id.substr is None:
                root.user_data.data_id = startID()
            return root

    elif username < root.username:
        data = createDatabase3(root.left, username, _id)

        if data != False:
            root.left = data
            return root

    elif username > root.username:
        data = createDatabase3(root.right, username, _id)

        if data != False:
            root.right = data
            return root

    return data


def createDatabase4(root, _id):
    if root is None:
        return User(_id, None, None, None, None)

    else:

        if root.database is None:
            return User(_id, None, None, None, None)

        else:

            if _id < root.database:
                data = createDatabase4(root.left, _id)

                if data != False:
                    root.left = data
                    root.left.data_id = startID()
                    return root

            elif _id > root.database:
                data = createDatabase4(root.right, _id)

                if data != False:
                    root.right = data
                    root.right.data_id = startID()
                    return root

            elif _id == root.database:
                data = False

            if data != False:
                root.height = 1 + max(getHeight(root.left), getHeight(root.right))

                balanceFactor = getBalance(root)

                if balanceFactor > 1:

                    if getBalance(root.left) >= 0:
                        return rightRotate(root)

                    else:
                        root.left = leftRotate(root)
                        return rightRotate(root)

                elif balanceFactor < -1:

                    if getBalance(root.right) <= 0:
                        return leftRotate(root)

                    else:
                        root.right = rightRotate(root.right)
                        return leftRotate(root)

            return data


# Database deletion
def deleteDatabase(root, api):
    username = api['username']
    database_id = api['database-id']

    root = deleteDatabase1(root, username, database_id)

    return root


def deleteDatabase1(root, username, _id):
    if username[0] == root.char:
        root.id = deleteDatabase2(root.id, username, _id)

    elif username[0] < root.char:
        root.left = deleteDatabase1(root.left, username, _id)

    elif username[0] > root.char:
        root.right = deleteDatabase1(root.right, username, _id)

    return root


def deleteDatabase2(root, username, _id):
    if len(username) == root.length:
        root.user_info = deleteDatabase3(root.user_info, username, _id)

    elif len(username) < root.length:
        root.left = deleteDatabase2(root.left, username, _id)

    elif len(username) > root.length:
        root.right = deleteDatabase2(root.right, username, _id)

    return root


def deleteDatabase3(root, username, _id):
    if username == root.username:
        root.user_data = deleteDatabase4(root.user_data, _id)

    elif username < root.username:
        root.left = deleteDatabase3(root.left, username, _id)

    elif username > root.username:
        root.right = deleteDatabase3(root.right, username, _id)

    return root


def deleteDatabase4(root, _id):
    if _id == root.database:

        if root.left is None:
            temp = root.right
            root = None
            return temp

        elif root.right is None:
            temp = root.left
            root = None
            return temp

        else:
            temp = getNode(root.right)
            root.database = temp.database
            root.data_id = temp.data_id
            root.right = deleteDatabase4(root.right, temp.database)

    elif _id < root.database:
        root.left = deleteDatabase4(root.left, _id)

    elif _id > root.database:
        root.right = deleteDatabase4(root.right, _id)

    if root is not None:
        return root

    root.height = 1 + max(getHeight(root.left), getHeight(root.right))

    balanceFactor = getBalance(root)

    if balanceFactor > 1:

        if getBalance(root.left) >= 0:
            return rightRotate(root)

        else:
            root.left = leftRotate(root)
            return rightRotate(root)

    elif balanceFactor < -1:

        if getBalance(root.right) <= 0:
            return leftRotate(root)

        else:
            root.right = rightRotate(root.right)
            return leftRotate(root)

    return root


# Data insertion
def insert(root, api, data):
    username = api['username']
    password = api['password']
    database_id = api['database-id']

    try:
        _id = data['_id'].lower()
        if _id[0] == "-":
            _id = "dataID-" + _id

        _id = re.sub('[^A-Za-z0-9.-]+', '', _id)

    except:
        _id = str(uuid.uuid4())

    data['_id'] = _id

    if password == getUserInfo(root, username):
        root = insert1(root, username, database_id, data, _id)

    return root


def insert1(root, username, _id, data, data_id):
    if username[0] == root.char:
        root.id = insert2(root.id, username, _id, data, data_id)

    elif username[0] < root.char:
        root.left = insert1(root.left, username, _id, data, data_id)

    elif username[0] > root.char:
        root.right = insert1(root.right, username, _id, data, data_id)

    return root


def insert2(root, username, _id, data, data_id):
    if len(username) == root.length:
        root.user_info = insert3(root.user_info, username, _id, data, data_id)

    elif len(username) < root.length:
        root.left = insert2(root.left, username, _id, data, data_id)

    elif len(username) > root.length:
        root.right = insert2(root.right, username, _id, data, data_id)

    return root


def insert3(root, username, _id, data, data_id):
    if username == root.username:
        root.user_data = insert4(root.user_data, _id, data, data_id)

    elif username < root.username:
        root.left = insert3(root.left, username, _id, data, data_id)

    elif username > root.username:
        root.right = insert3(root.right, username, _id, data, data_id)

    return root


def insert4(root, _id, data, data_id):
    if _id == root.database:
        root.data_id = insert5(root.data_id, data, data_id)

    elif _id < root.database:
        root.left = insert4(root.left, _id, data, data_id)

    elif _id > root.database:
        root.right = insert4(root.right, _id, data, data_id)

    return root


def insert5(root, data, _id):
    if _id[0] == root.substr:
        root.sub_id = insert6(root.sub_id, data, _id)

    elif _id[0] < root.substr:
        root.left = insert5(root.left, data, _id)

    elif _id[0] > root.substr:
        root.right = insert5(root.right, data, _id)

    return root


def insert6(root, data, _id):
    if root is None:
        return Sub_ID(len(_id), _id, data)

    else:

        if root.sub_length is None:
            root.sub_length = len(_id)
            root.data_tree = Data(_id, data)

        else:

            if len(_id) == root.sub_length:
                root.data_tree = insert7(root.data_tree, data, _id)

            elif len(_id) < root.sub_length:
                root.left = insert6(root.left, data, _id)

            elif len(_id) > root.sub_length:
                root.right = insert6(root.right, data, _id)

        root.height = 1 + max(getHeight(root.left), getHeight(root.right))

        balanceFactor = getBalance(root)

        if balanceFactor > 1:

            if getBalance(root.left) >= 0:
                return rightRotate(root)

            else:
                root.left = leftRotate(root)
                return rightRotate(root)

        elif balanceFactor < -1:

            if getBalance(root.right) <= 0:
                return leftRotate(root)

            else:
                root.right = rightRotate(root.right)
                return leftRotate(root)

        return root


def insert7(root, data, _id):
    if root is None:
        return Data(_id, data)

    else:

        if root._id is None:
            return Data(_id, data)

        else:

            if _id == root._id:
                root.data = data
                return root

            elif _id < root._id:
                root.left = insert7(root.left, data, _id)

            elif _id > root._id:
                root.right = insert7(root.right, data, _id)

            root.height = 1 + max(getHeight(root.left), getHeight(root.right))

            balanceFactor = getBalance(root)

            if balanceFactor > 1:

                if getBalance(root.left) >= 0:
                    return rightRotate(root)

                else:
                    root.left = leftRotate(root)
                    return rightRotate(root)

            elif balanceFactor < -1:

                if getBalance(root.right) <= 0:
                    return leftRotate(root)

                else:
                    root.right = rightRotate(root.right)
                    return leftRotate(root)

            return root


# Data deletion
def delete(root, api, _id):
    username = api['username']
    password = api['password']
    database_id = api['database-id']

    if password == getUserInfo(root, username):
        root = delete1(root, username, database_id, _id)

    return root


def delete1(root, username, _id, data_id):
    if username[0] == root.char:
        root.id = delete2(root.id, username, _id, data_id)

    elif username[0] < root.char:
        root.left = delete1(root.left, username, _id, data_id)

    elif username[0] > root.char:
        root.right = delete1(root.right, username, _id, data_id)

    return root


def delete2(root, username, _id, data_id):
    if len(username) == root.length:
        root.user_info = delete3(root.user_info, username, _id, data_id)

    elif len(username) < root.length:
        root.left = delete2(root.left, username, _id, data_id)

    elif len(username) > root.length:
        root.right = delete2(root.right, username, _id, data_id)

    return root


def delete3(root, username, _id, data_id):
    if username == root.username:
        root.user_data = delete4(root.user_data, _id, data_id)

    elif username < root.username:
        root.left = delete3(root.left, username, _id, data_id)

    elif username > root.username:
        root.right = delete3(root.right, username, _id, data_id)

    return root


def delete4(root, _id, data_id):
    if _id == root.database:
        root.data_id = delete5(root.data_id, data_id)

    elif _id < root.database:
        root.left = delete4(root.left, _id, data_id)

    elif _id > root.database:
        root.right = delete4(root.right, _id, data_id)

    return root


def delete5(root, _id):
    if _id[0] == root.substr:
        root.sub_id = delete6(root.sub_id, _id)

    elif _id[0] < root.substr:
        root.left = delete5(root.left, _id)

    elif _id[0] > root.substr:
        root.right = delete5(root.right, _id)

    return root


def delete6(root, _id):
    if len(_id) == root.sub_length:
        root.data_tree = delete7(root.data_tree, _id)

    elif len(_id) < root.sub_length:
        root.left = delete6(root.right, _id)

    elif len(_id) > root.sub_length:
        root.right = delete6(root.right, _id)

    return root


def delete7(root, _id):
    if _id == root._id:

        if root.left is None:
            temp = root.right
            root = None
            return temp

        elif root.right is None:
            temp = root.left
            root = None
            return temp

        else:
            temp = getNode(root.right)
            root._id = None
            root._id = temp._id
            root.data = None
            root.data = temp.data
            root.right = delete7(root.right, temp._id)

    elif _id < root.database:
        root.left = delete7(root.left, _id)

    elif _id > root.database:
        root.right = delete7(root.right, _id)

    if root is not None:
        return root

    root.height = 1 + max(getHeight(root.left), getHeight(root.right))

    balanceFactor = getBalance(root)

    if balanceFactor > 1:

        if getBalance(root.left) >= 0:
            return rightRotate(root)

        else:
            root.left = leftRotate(root)
            return rightRotate(root)

    elif balanceFactor < -1:

        if getBalance(root.right) <= 0:
            return leftRotate(root)

        else:
            root.right = rightRotate(root.right)
            return leftRotate(root)

    return root


# Data search
def search(root, api, _id):
    username = api['username']
    password = api['password']
    database_id = api['database-id']

    if password == getUserInfo(root, username):
        data = search1(root, username, database_id, _id)
        return data

    else:
        return {}


def search1(root, username, _id, data_id):
    if username[0] == root.char:
        data = search2(root.id, username, _id, data_id)

    elif username[0] < root.char:
        data = search1(root.left, username, _id, data_id)

    elif username[0] > root.char:
        data = search1(root.right, username, _id, data_id)

    return data


def search2(root, username, _id, data_id):
    if len(username) == root.length:
        data = search3(root.user_info, username, _id, data_id)

    elif len(username) < root.length:
        data = search2(root.left, username, _id, data_id)

    elif len(username) > root.length:
        data = search2(root.right, username, _id, data_id)

    return data


def search3(root, username, _id, data_id):
    if username == root.username:
        data = search4(root.user_data, _id, data_id)

    elif username < root.username:
        data = search3(root.left, username, _id, data_id)

    elif username > root.username:
        data = search3(root.right, username, _id, data_id)

    return data


def search4(root, _id, data_id):
    if _id == root.database:
        data = search5(root.data_id, data_id)

    elif _id < root.database:
        data = search4(root.left, _id, data_id)

    elif _id > root.database:
        data = search4(root.right, _id, data_id)

    return data


def search5(root, _id):
    if _id[0] == root.substr:
        data = search6(root.sub_id, _id)

    elif _id[0] < root.substr:
        data = search5(root.left, _id)

    elif _id[0] > root.substr:
        data = search5(root.right, _id)

    return data


def search6(root, _id):
    if len(_id) == root.sub_length:
        data = search7(root.data_tree, _id)

    elif len(_id) < root.sub_length:
        data = search6(root.right, _id)

    elif len(_id) > root.sub_length:
        data = search6(root.right, _id)

    return data


def search7(root, _id):
    if root is None:
        return {}

    else:

        if _id == root._id:
            return {root._id: root.data}

        elif _id < root.left:
            data = search7(root.left, _id)

        elif _id > root.right:
            data = search7(root.right, _id)

        return data


# Tree balacing
def getHeight(root):
    if not root:
        return 0
    return root.height


def getBalance(root):
    if not root:
        return 0
    return getHeight(root.left) - getHeight(root.right)


# Rotation
def rightRotate(node):
    y = node.left
    x = y.right
    y.right = node
    node.left = x
    node.height = 1 + max(getHeight(node.left), getHeight(node.right))
    y.height = 1 + max(getHeight(y.left), getHeight(y.right))
    return y


def leftRotate(node):
    y = node.right
    x = y.left
    y.left = node
    node.right = x
    node.height = 1 + max(getHeight(node.left), getHeight(node.right))
    y.height = 1 + max(getHeight(y.left), getHeight(y.right))
    return y


def getNode(root):
    if root is None or root.left is None:
        return root
    return getNode(root.left)


# Get database names
def getDatabase(root, api):
    username = api['username']
    password = api['password']

    if password == getUserInfo(root, username):
        data = getDatabase1(root, username)
        return data

    else:
        return []


def getDatabase1(root, username):
    if username[0] == root.char:
        data = getDatabase2(root.id, username)

    elif username[0] < root.char:
        data = getDatabase1(root.left, username)

    elif username[0] > root.char:
        data = getDatabase1(root.right, username)

    return data


def getDatabase2(root, username):
    if len(username) == root.length:
        data = getDatabase3(root.user_info, username)

    elif len(username) < root.length:
        data = getDatabase2(root.left, username)

    elif len(username) > root.length:
        data = getDatabase2(root.right, username)

    return data


def getDatabase3(root, username):
    if username == root.username:
        data = getDatabase4(root.user_data, [])

    elif username < root.username:
        data = getDatabase3(root.left, username)

    elif username > root.username:
        data = getDatabase3(root.right, username)

    return data


def getDatabase4(root, data):
    if root is None:
        return data

    else:
        data = getDatabase4(root.left, data)
        data.append(root.database)
        data = getDatabase4(root.right, data)
        return data


# Get data
def getData(root, api):
    try:
        username = api['username']
        password = api['password']
        database_id = api['database-id']

        if password == getUserInfo(root, username):
            data = getData1(root, username, database_id)
            data.pop(None)
            return data

    except:
        return None


def getData1(root, username, _id):
    if username[0] == root.char:
        data = getData2(root.id, username, _id)

    elif username[0] < root.char:
        data = getData1(root.left, username, _id)

    elif username[0] > root.char:
        data = getData1(root.right, username, _id)

    return data


def getData2(root, username, _id):
    if len(username) == root.length:
        data = getData3(root.user_info, username, _id)

    elif len(username) < root.length:
        data = getData2(root.left, username, _id)

    elif len(username) > root.length:
        data = getData2(root.right, username, _id)

    return data


def getData3(root, username, _id):
    if username == root.username:
        data = getData4(root.user_data, _id)

    elif username < root.username:
        data = getData3(root.left, username, _id)

    elif username > root.username:
        data = getData3(root.right, username, _id)

    return data


def getData4(root, _id):
    if _id == root.database:
        data = getData5(root.data_id, {})

    elif _id < root.database:
        data = getData4(root.left, _id)

    elif _id > root.database:
        data = getData4(root.right, _id)

    return data


def getData5(root, data):
    if root is None:
        return data

    else:
        data = getData5(root.left, data)
        data = getData6(root.sub_id, data)
        data = getData5(root.right, data)
        return data


def getData6(root, data):
    if root is None:
        return data

    else:
        data = getData6(root.left, data)
        data = getData7(root.data_tree, data)
        data = getData6(root.right, data)
        return data


def getData7(root, data):
    if root is None:
        return data

    else:
        data = getData7(root.left, data)
        data[root._id] = root.data
        data = getData7(root.right, data)
        return data


# Get total number of users
def getNumofUser(root, num):
    if root is None:
        return num

    else:
        num = getNumofUser(root.left, num)
        num = getNumofUser1(root.id, num)
        num = getNumofUser(root.right, num)
        return num


def getNumofUser1(root, num):
    if root is None:
        return num

    else:
        num = getNumofUser1(root.left, num)
        num = getNumofUser2(root.user_info, num)
        num = getNumofUser1(root.right, num)
        return num


def getNumofUser2(root, num):
    if root is None:
        return num

    else:
        num = getNumofUser2(root.left, num)
        if root.username is not None:
            num += 1
        num = getNumofUser2(root.right, num)
        return num


# Initalization
root = startDatabase(None)
api = {'username': 'codejapoe', 'password': 'Hackcode'}
data = createAccount(root, api)
if data is not False:
    root = data
api['database-id'] = 'akkdb'
root = createDatabase(root, api)
root = insert(root, api, {"name":"Aung", "_id":"iee"})
root = insert(root, api, {"name":"Noel", "_id":"noel"})
api['database-id'] = 'nullbytesdb'
root = createDatabase(root, api)
root = insert(root, api, {"name":"Mario", "_id":"mario"})
root = insert(root, api, {"age":"17", "_id":"iee"})
print(root)