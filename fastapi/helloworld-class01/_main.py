from fastapi import FastAPI

app = FastAPI()

@app.get("/person")
def hello_person():
    return {"message": "Hello person"}

@app.get("/class")
def hello_class():
    return {"message": "Hello class"}

@app.get("/person/{person_name}")
def hello_person(person_name):
    return {"message": "Hello person : "+person_name}
