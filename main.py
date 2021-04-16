from bson import ObjectId
from pymongo import MongoClient

host = '127.0.0.1'
username = 'root'
password = '|cSFu@5rFv#h8*='
connectTimeoutMS = 10000
authMechanism = 'SCRAM-SHA-1'
authSource = 'admin'
serverSelectionTimeoutMS = 5000
port = 12220
client = MongoClient(
    host=host,
    username=username,
    password=password,
    authSource=authSource,
    port=port,
    serverSelectionTimeoutMS=serverSelectionTimeoutMS,
    connectTimeoutMS=connectTimeoutMS,
    authMechanism=authMechanism
)
database = client['DigisatServer']
cursor = database["Estoques"].find({})

EstoqueInsert = []
try:
    for doc in cursor:
        EstoqueTotal = 0
        cont = -1
        Keyinicial = -1
        for Quantidade in doc['Quantidades']:
            cont += 1
            EstoqueTotal += Quantidade['Quantidade']
            if 'EstoqueQuantidade' == Quantidade['_t'] or 'EstoqueQuantidade' in Quantidade['_t']:
                Keyinicial = cont

        if EstoqueTotal != 0:
            if Keyinicial == -1:
                template = dict(
                    _t="EstoqueQuantidade",
                    _id=ObjectId(),
                    InformacoesPesquisa=[],
                    EstoqueReferencia=doc['_id'],
                    EstoqueReferenciaParent=doc['_id'],
                    Quantidade=EstoqueTotal * -1
                )
                doc['Quantidades'].append(template)
                database["EstoquesQuantidade"].insert_one(template)
                database["Estoques"].update_one({'_id': doc['_id']}, {'$set': doc})
            else:
                doc['Quantidades'][Keyinicial]['Quantidade'] += EstoqueTotal * -1
                database["Estoques"].update_one({'_id': doc['_id']}, {'$set': doc})
finally:
    client.close()
