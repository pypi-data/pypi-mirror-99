```python
with open("test.pdf", "rb") as inFile, open("modified.pdf", "wb") as modified:
    modified.write(
        sign("Дик Анатолий Артёмович",
             datetime(2020, 1, 25, 0, 0),
             "123asdfdfsddfasdf62gdsfgsd45345", inFile)
            .getvalue())

```
