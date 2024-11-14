from typing import Dict, List, Tuple
from collections import defaultdict
from dataclasses import dataclass
import csv
# T1: Estructuramos los datos 
@dataclass
class VoteRecord:
    city: str
    candidate: str
    votes: int

# T2:  Encapsulación 
class VoteCounter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        # T3: simplificar la lógica de conteo 
        self.results: Dict[str, int] = defaultdict(int)

    #  T4: Unica función 
    def process_vote_row(self, row: List[str]) -> VoteRecord:
        try:
            votes = max(0, int(row[2]))  
        except (ValueError, IndexError):
            votes = 0
        return VoteRecord(city=row[0], candidate=row[1], votes=votes)

    # T5: Manejo de errores  
    def count_votes(self) -> Tuple[Dict[str, int], List[str]]:
        try:
            with open(self.file_path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader)  
                
                for row in reader:
                    record = self.process_vote_row(row)
                    self.results[record.candidate] += record.votes

            winners = self.get_winners()
            self.print_results(winners)
            return self.results, winners
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {self.file_path}")
        except csv.Error:
            raise ValueError("Error al procesar el archivo CSV")

    def get_winners(self) -> List[str]:
        if not self.results:
            return []
            
        max_votes = max(self.results.values())
        return [candidate for candidate, votes in self.results.items() 
                if votes == max_votes]

    def print_results(self, winners: List[str]) -> None:
        for candidate, votes in self.results.items():
            print(f"{candidate}: {votes} votes")
        
        if len(winners) > 1:
            print(f"Empate entre: {', '.join(winners)}")
        elif winners:
            print(f"winner is {winners[0]}")


if __name__ == "__main__":
    counter = VoteCounter('votes.csv')
    counter.count_votes()