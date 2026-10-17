import json
class TaskNotFound(Exception):
    pass
class TaskAlreadyExists(Exception):
    pass
class Task:
    def __init__(self, id,title,done=False):
        self.title = title
        self.id =id 
        self.done = done
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    def add_task(self, title):
        task = Task(self.next_id, title)
        self.tasks.append(task)
        self.next_id += 1 
    def complete(self,taskid):
        for task in self.tasks:
            if task.id == taskid:
                task.done = True
                return
        raise TaskNotFound(f"Task with id {taskid} not found.")
    def list_task(self):
        for i in self.tasks:
            status = "Done" if i.done else "Not Done"
            print(f"ID: {i.id}, Title: {i.title}, Status: {status}")
    def delete(self,taskid):
        for task in self.tasks:
            if task.id==taskid:
                self.tasks.remove(task)
                return
        raise TaskNotFound(f"Task with id {taskid} not found.")
    def save(self):
        data = []
        for t in self.tasks:
            data.append({"id": t.id, "title": t.title, "done": t.done})
        with open("tasks.json", "w") as f:
            json.dump(data, f)
    def load(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        self.tasks = [Task(d["id"], d["title"], d["done"]) for d in data]
        self.next_id = max((t.id for t in self.tasks), default=0) + 1

def main():
    tm=TaskManager()
    tm.load()
    while 1:
        c=input("Enter command (add/list/complete/delete/exit): ").strip().lower()
        if c =="add":
            title=input("Enter task title: ")
            tm.add_task(title)
            tm.save()
        elif c=="list":
            tm.list_task()
        elif c=="complete":
            try:
                taskid=int(input("Enter task id to complete: "))
                tm.complete(taskid)
                tm.save()
            except TaskNotFound as e:
                print(e)
            except ValueError:
                print("Please enter a number.")
        elif c=="delete":
            try:
                taskid=int(input("Enter task id to delete: "))
                tm.delete(taskid)
                tm.save()
            except TaskNotFound as q:
                print(q)
            except ValueError:
                print("Please enter a number.")   
        elif c=="exit":
            break
        else:
            print("unknown command")
if __name__=="__main__":
    main()

