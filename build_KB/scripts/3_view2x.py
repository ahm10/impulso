
'''
Objective: Check the data ingestion by testing view queries. 
Run from the root
$ python ./build_KB/scripts/3_view.py
$ python ROOT_DIR/WIKI_DIR/SCRIPTS_DIR/filename.py

'''
import configparser


config = configparser.ConfigParser()

config_path = '../config.ini'

config.read(config_path)

GRAKN_URI = config['GRAKN_CONNECTION']['uri']

GRAKN_KS = config['GRAKN_CONNECTION']['ks']



from grakn.client import GraknClient

with GraknClient(uri=GRAKN_URI) as client:
    with client.session(keyspace = GRAKN_KS) as session:
        with session.transaction().read() as transaction:
            test_topic = "Artificial_intelligence"
            # query = [
            #     'match',
            #     '  $topic isa topic, has title "' + test_topic +  '" has txt $x;',
        

            #     'get $txt;'
            # ]

            # print(">>> Get first level child nodes of topic: ", test_topic)

            # query = "".join(query)

            # print("\nExecuting Query:\n", "\n".join(query))


            # iterator = transaction.query(query)
            # answers = [ans.get("x") for ans in iterator]
            # result = [ answer.value() for answer in answers ]

            # print("\nResult:\n", result)

            print("---------------------------")
            query1 = [
                'match',
                '  $t1 isa Tparent, has title "' + test_topic.lower() + '", has UUID $x;',
                'get $x;'
            ]

            print("\nExecuting Query:\n", "\n".join(query1))
            query1 = "".join(query1)

 
 
            iterator = transaction.query(query1)
            answers = [ans.get("x") for ans in iterator]
            result = [ answer.value() for answer in answers ]

            topic_UUID = result[0]

            print("\nResult:\n", topic_UUID)

            print("---------------------------")
            query1 = [
                'match',
                '  $t1 isa Tparent, has title "' + test_topic.lower() + '", has UUID $x;',
                'get $x;'
            ]

            print("---------------------------")
            query2 = [
                'match',
                '  $t1 isa Tparent, has UUID "' + topic_UUID + '";',
                '  $t2 isa article, has title $x;'
                '  (parent: $t1, supplement: $t2) isa ExplainedIn, has content $c;',
                'get $x;'
            ]

            print("\nExecuting Query:\n", "\n".join(query2))
            query2 = "".join(query2) 

            iterator = transaction.query(query2)
            answers = [ans.get("x") for ans in iterator]
            result = [ answer.value() for answer in answers ]

            print("\nResult:\n", result)

