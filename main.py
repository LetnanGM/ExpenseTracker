import sys
import logging

from typing import Any, Dict
from datetime import datetime
from argparse import ArgumentParser, Namespace

from pydantic import BaseModel

isoload = lambda x: datetime.fromisoformat(x)

# setup logging here :V
# its capture ERROR, not logging your keyboard beach.
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s"
)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logging.error("Uncaught exception: ", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception
    
class Model(BaseModel):
    description  :   str
    amount       :   int
    date         :   str
    date_raw     :   str
    
    @classmethod
    def to_dict(cls, model) -> Dict[str, str | int]:
        return dict(
            description=model.description,
            amount=model.amount,
            date=model.date,
            date_raw=model.date_raw
        )
        
class DBHandler:
    def __init__(self):
        self.memory: Dict[Any, Any] = {}
        self.index: int = 1
        self.load_db()
        
    def load_db(self):
        import json
        
        try:
            with open("expense_db.json", "r") as fp:
                raw = json.load(fp=fp)
                # normalize keys to int (json saves keys as string)
                self.memory = {int(k): v for k, v in raw.items()}
                self.index = max(self.memory.keys(), default=0) + 1
                
        except FileNotFoundError:
            print("[*] No restored data yet. New session!")
        
    def save_db(self):
        import json
        try:
            with open("expense_db.json", "w") as fp:
                json.dump(obj=self.memory, fp=fp, indent=4)    
        except json.JSONDecodeError:
            print("[!] Report this problem to developer issue on github! \n")
            
    def create(self, description: str, amount: int) -> bool:
        date = str(datetime.now().strftime(format="%d-%m-%Y"))
        date_raw = str(datetime.now().isoformat())
        
        data = dict(description=description,amount=amount,date=date,date_raw=date_raw)
        model = Model(**data)
        
        self.memory[self.index] = model.to_dict(model=model)
        print(f"[*] Expense added successfully (ID {self.index})")
        self.index += 1
        self.save_db()
        
        return True
        
    def read(self):
        return ReadHandler
        
    def update(self, index: int, model: Model) -> bool:
        def date(index: int, model: Model):
            date = model.date
            raw = model.date_raw
            
            data = self.memory[index]
            if data["date"] != date or data["date_raw"] != raw:
                raise ValueError(f"Date cannot be modified.")
            
            return None
        
        # FIX: isinstance butuh 2 argumen
        if not index or not isinstance(index, int):
            raise ValueError(f"maybe `index`:{index} is empty or index are not integer.")
        
        if not model:
            raise ValueError(f"Model must be field!")
        
        if not index in self.memory.keys():
            return False
        
        date(index=index, model=model)
        self.memory[index] = model.to_dict(model=model)
        self.save_db()
        
        return True
    
    def delete(self, index: int) -> bool:
        if not index:
            return False
        
        if not index in self.memory.keys():
            print(f"[+] ID-{index} are not in our record!")
            return True
        
        del self.memory[index]
        print(f"[*] Deleted successfully (ID {index})")
        
        self.save_db()
        return True


class Viewer:
    
    @staticmethod
    def view(data: Dict[str | int, str | int] = None, json: bool = False) -> Dict[str | int, str | int] | None:
        # FIX: pakai data yg sudah difilter, udah ga paksa makek database.memory :D
        dat = data
        if not dat:
            print("[*] No data to display.")
            return
        
        if json:
            import json as json_convert
            return json_convert.dumps(dat, indent=4)
        
        print(f"{'ID':<5}{'DATE':<15}{'Description':<15}{'Amount':<15}")
        print("-" * 40)
        
        for id, value in dat.items():
            model = Model(**value)
            print(f"{id:<5}{model.date:<15}{model.description:<15}{model.amount:<15}")
    
    @staticmethod
    def summary_date(data: Dict, condition, json: bool = False):
        result = {
            k: v for k, v in data.items()
            if condition(v)
        }
        
        Viewer.view(data=result, json=json)
        
    @staticmethod
    def summary_total(data: Dict[str | int, str | int]):
        totals: int = 0
        
        print("[+] Counting your expense..")
        for id, value in data.items():
            model = Model(**value)
            totals += model.amount
            
        print(f"Total expense: ${totals}")
        return totals
        
class ReadHandler:
    @staticmethod
    def view_all(data: Dict[str | int, str | int] = None, json: bool = False) -> Dict[str, str | int] | None:
        return Viewer.view(data, json)
            
    @staticmethod
    def summary(data: Dict[str | int, str | int]) -> int:
        return Viewer.summary_total(data=data)
    
    @staticmethod
    def summary_day(data: Dict, day: int, json: bool = False): 
        return Viewer.summary_date(
            data=data,
            condition=lambda v: isoload(v["date_raw"]).day == day,
            json=json
        )
        
    @staticmethod
    def summary_month(data: Dict, month: int, json: bool = False): 
        return Viewer.summary_date(
            data=data,
            condition=lambda v: isoload(v["date_raw"]).month == month,
            json=json
        )
        
    @staticmethod
    def summary_year(data: Dict, year: int, json: bool = False): 
        return Viewer.summary_date(
            data=data,
            condition=lambda v: isoload(v["date_raw"]).year == year,
            json=json
        )
        
    @staticmethod
    def summary_combination(data: Dict, args: Namespace) -> bool:
        # FIX: filter dulu semua, baru tampilkan sekali — bukan loop + early return
        def match(expense):
            if args.day is not None and isoload(expense["date_raw"]).day != args.day:
                return False
            if args.month is not None and isoload(expense["date_raw"]).month != args.month:
                return False
            if args.year is not None and isoload(expense["date_raw"]).year != args.year:
                return False
            return True
        
        result = {k: v for k, v in data.items() if match(v)}
        
        if not result:
            print("[*] Data are not available.")
            return False
        
        Viewer.view(data=result)
        Viewer.summary_total(data=result)
        return True
    
class COLIST:
    def __init__(self, co) -> None:
        self.co = co
        self.db = DBHandler()
        
    def add(self):
        desc = self.co.description
        # FIX: amount dari argparse itu str, cast ke int
        
        try:
            amount = int(self.co.amount)
        except ValueError:
            print("[!] Amount must be number")
            return
        
        self.db.create(desc, amount)
        
    def delete(self):
        # FIX: id dari argparse itu str, cast ke int
        idx = int(self.co.id)
        self.db.delete(idx)
        
    def co_list(self):
        self.db.read().view_all(data=self.db.memory, json=False)
        
    def summary(self):
        # FIX: harusnya self.co (Namespace), bukan self.co_list (method)
        ReadHandler.summary_combination(
            data=self.db.memory,
            args=self.co
        )
    
class COHandler:
    def __init__(self, parser: ArgumentParser):
        self.co: Namespace = parser.parse_args()
        
    def parse(self):
        co = COLIST(self.co)
        keyMap = {
            "add": co.add,
            "delete": co.delete,
            "list": co.co_list,
            "summary": co.summary
        }
        
        if self.co.command.lower() in keyMap.keys():
            instance = keyMap.get(self.co.command.lower())
            # FIX: load_db() tidak ada, DB sudah di-load di DBHandler.__init__
            instance()
        else:
            print("Return: Unknown command, available [add, delete, list, summary]")
    
def setup_argparse():
    parser = ArgumentParser(prog="Welcome to expense simple tracker.")
    subparsers = parser.add_subparsers(dest="command")
    
    add_parser = subparsers.add_parser("add")
    delete_parser = subparsers.add_parser("delete")
    list_parser = subparsers.add_parser("list")
    summary_parser = subparsers.add_parser("summary")
    
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", required=True)
    delete_parser.add_argument("--id", required=True)
    
    summary_parser.add_argument("--day", required=False, type=int)
    summary_parser.add_argument("--month", required=False, type=int)
    summary_parser.add_argument("--year", required=False, type=int)
    
    COHandler(parser=parser).parse()
    
if __name__ == '__main__':
    setup_argparse()