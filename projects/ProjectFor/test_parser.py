from hltv_parser import HLTVParser
import json

def test_parser():
    parser = HLTVParser()
    matches = parser.get_upcoming_matches()
    
    # Сохраняем результаты в файл
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
        
    print(f"Найдено матчей: {len(matches)}")
    
    # Выводим первые 3 матча для проверки
    for match in matches[:3]:
        print(f"\nМатч: {match['team1']} vs {match['team2']}")
        print(f"Турнир: {match['tournament']}")
        print(f"Формат: {match['format']}")
        print(f"Дата: {match['date']}")
        print(f"URL: {match['url']}")

if __name__ == '__main__':
    test_parser() 