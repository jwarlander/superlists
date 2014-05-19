## TODO

-   Make form.save() create a list if not given as arg?
-   Use some kind of hash as URL key to a list, not the id
-   Make it possible to delete lists
-   Allow checking items off
-   NOT HAPPY with functional_tests/test_login.py
    -    test doesn't fail properly even if Persona logout is skipped
         in favor of only doing a Django logout
    -    it does seem to crash Django at that point, though..?
-   Look at alternative mocking frameworks; unittest.mock feels somewhat
    confusing in some use cases..
-   Use PostreSQL database deployed on separate server
-   Add static HTML page showing "work in progress" if Gunicorn down
-   Go for HTTPS instead, maybe with a "real" certificate


## Done

-   Support more than one list!
-   Display multiple items in the table
-   Code smell: POST test is too long?
-   Don’t save blank items for every request
