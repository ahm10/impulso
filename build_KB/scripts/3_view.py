
'''
Objective: Check the data ingestion by testing view queries. 
Run from the root
$ python ./build_KB/scripts/3_view.py
$ python ROOT_DIR/WIKI_DIR/SCRIPTS_DIR/filename.py

'''




from grakn.client import GraknClient

with GraknClient(uri="localhost:48555") as client:
    with client.session(keyspace = "impulso2") as session:
        with session.transaction().read() as transaction:
            test_topic = "Machine_learning"
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
                '  $t1 isa Tparent, has title "' + test_topic + '";',
                '  $t2 isa Tchild, has title $x;'
                '  (parent: $t1, child: $t2) isa ConsistsOf;',
                'get $x;'
            ]

            print("\nExecuting Query:\n", "\n".join(query1))
            query1 = "".join(query1)

            iterator = transaction.query(query1)
            answers = [ans.get("x") for ans in iterator]
            result = [ answer.value() for answer in answers ]

            test_child_topic = result[0]

            print("\nResult:\n", result)

            print("---------------------------")
            query2 = [
                'match',
                '  $t1 isa Tparent, has title "' + test_topic + '";',
                '  $t2 isa Tchild, has title "' + test_child_topic + '";'
                '  (parent: $t1, child: $t2) isa ConsistsOf, has content $x;',
                'get $x;'
            ]

            print("\nExecuting Query:\n", "\n".join(query2))
            query2 = "".join(query2)

            iterator = transaction.query(query2)
            answers = [ans.get("x") for ans in iterator]
            result = [ answer.value() for answer in answers ]

            print("\nResult:\n", result)


            
            print("---------------------------")

            # test_child_topic = "Models"
            query22 = [
                'match',
                
                '  $t2 isa Tparent, has title "' + test_child_topic + '";',
                '  $t3 isa Tchild, has title $x;'
                '  $r(parent: $t2, child: $t3) isa ConsistsOf;',
                'get $x;'
            ]

            print("\nExecuting Query:\n", "\n".join(query22))
            query22 = "".join(query22)

            iterator = transaction.query(query22)
            answers = [ans.get("x") for ans in iterator]
            result = [ answer.value() for answer in answers ]

            print("\nResult:\n", result)




            # test_subtopic1 = "Overview"

            # print(">>> Get parent of test subtopic: ", test_subtopic1)

            # query2 = [
            #     'match',
            #     '  $p1 isa subtopic1, has title "'+ test_subtopic1 +'";',
            #     '  $p0 isa topic, has title $x;',
            #     '  $r (level0: $p0, level1: $p1);',

            #     'get $p0,$x;'
            # ]

            # print("\nExecuting Query:\n", "\n".join(query2))
            # query2 = "".join(query2)
            
            # iterator = transaction.query(query2)
 
            # answers = [ans.get("x") for ans in iterator]
            # result = [ answer.value() for answer in answers ]

            # print("\nResult:\n", result)

            # print("---------------------------")


            # print(">>> Get list of headers under " + test_topic + "->" + test_subtopic1)        
 
            # query3 = [
            #     'match',
            #     '  $p2 isa subtopic2, has title $x;',
            #     '  $p1 isa subtopic1, has title "Overview";',
            #     '  $p0 isa topic, has title "Machine_learning";',
            #     '  $r1 (level0: $p0, level1: $p1);',
            #     '  $r2 (level1: $p1, level2: $p2);',
            #     'get $x;'
            # ]

            # print("\nExecuting Query:\n", "\n".join(query3))
            # query3 = "".join(query3)
            
            # iterator = transaction.query(query3)
            # answers = [ans.get("x") for ans in iterator]
            # result = [ answer.value() for answer in answers ]

            # print("\nResult:\n", result)
 
            # test_subtopic1 = "History and relationships to other fields"

            # print(">>> Get content under " + test_topic + "->" + test_subtopic1)        

            
            # query4 = [
            #     'match',
            #      ' $p1 isa subtopic1, has title "'+ test_subtopic1 +'", has txt $x ;',
            #     '  $p0 isa topic, has title "'+ test_topic +'";',
            #     '  $r1 (level0: $p0, level1: $p1);',
            #     'get $x;'
            # ]

            # print("\nExecuting Query:\n", "\n".join(query4))
            # query4 = "".join(query4)
            
            # iterator = transaction.query(query4)
            # answers = [ans.get("x") for ans in iterator]
            # result = [ answer.value() for answer in answers ]

            # print("\nResult:\n", result)
 

