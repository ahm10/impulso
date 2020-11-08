from grakn.client import GraknClient

with GraknClient(uri="localhost:48555") as client:
    with client.session(keyspace = "zeitlabs") as session:
        with session.transaction().read() as transaction:
            # query = [
            #     'match',
            #     '  $topic isa topic, has txt $txt;',
        

            #     'get $txt;'
            # ]

            test_topic = "Machine_learning"
            print(">>> Get first level child nodes of topic: ", test_topic)
            query1 = [
                'match',
                '  $p1 isa subtopic1, has title $x;',
                '  $p0 isa topic, has title "'+ test_topic +'" ;',
                '  $r (level0: $p0, level1: $p1);',

                'get $x;'
            ]

            print("\nExecuting Query:\n", "\n".join(query1))
            query1 = "".join(query1)

            iterator = transaction.query(query1)
            answers = [ans.get("x") for ans in iterator]
            result = [ answer.value() for answer in answers ]

            print("\nResult:\n", result)

            print("---------------------------")

            test_subtopic1 = "Overview"

            print(">>> Get parent of test subtopic: ", test_subtopic1)

            query2 = [
                'match',
                '  $p1 isa subtopic1, has title "'+ test_subtopic1 +'";',
                '  $p0 isa topic, has title $x;',
                '  $r (level0: $p0, level1: $p1);',

                'get $p0,$x;'
            ]

            print("\nExecuting Query:\n", "\n".join(query2))
            query2 = "".join(query2)
            
            iterator = transaction.query(query2)
 
            answers = [ans.get("x") for ans in iterator]
            result = [ answer.value() for answer in answers ]

            print("\nResult:\n", result)

            print("---------------------------")


            print(">>> Get list of headers under " + test_topic + "->" + test_subtopic1)        
 
            query3 = [
                'match',
                '  $p2 isa subtopic2, has title $x;',
                '  $p1 isa subtopic1, has title "Overview";',
                '  $p0 isa topic, has title "Machine_learning";',
                '  $r1 (level0: $p0, level1: $p1);',
                '  $r2 (level1: $p1, level2: $p2);',
                'get $x;'
            ]

            print("\nExecuting Query:\n", "\n".join(query3))
            query3 = "".join(query3)
            
            iterator = transaction.query(query3)
            answers = [ans.get("x") for ans in iterator]
            result = [ answer.value() for answer in answers ]

            print("\nResult:\n", result)
 
            test_subtopic1 = "History and relationships to other fields"

            print(">>> Get content under " + test_topic + "->" + test_subtopic1)        

            
            query4 = [
                'match',
                 ' $p1 isa subtopic1, has title "'+ test_subtopic1 +'", has txt $x ;',
                '  $p0 isa topic, has title "'+ test_topic +'";',
                '  $r1 (level0: $p0, level1: $p1);',
                'get $x;'
            ]

            print("\nExecuting Query:\n", "\n".join(query4))
            query4 = "".join(query4)
            
            iterator = transaction.query(query4)
            answers = [ans.get("x") for ans in iterator]
            result = [ answer.value() for answer in answers ]

            print("\nResult:\n", result)
 

