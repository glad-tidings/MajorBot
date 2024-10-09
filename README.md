# MajorBot
MajorBot Auto Farm

# Features
| Feature                   | Supported |
| :------------------------ | :-------- |
| Multithreading            | ✅        |
| Auto Claim Task           | ✅        |
| Auto Roulette             | ✅        |
| Auto Hold Coins           | ✅        |
| Auto Swipe Coins          | ✅        |
| Auto Puzzle Pavel         | ✅        |
| Auto Daily Streak         | ✅        |
| Support pyrogram .session | ✅        |

## Settings
open Major.py with text editor and find
'''python
major_queries.append(MajorQuery(0, "Account 1", "query_id"))
'''
for each account you need to add an append in a new line, for example for 3 accounts:
'''python
major_queries.append(MajorQuery(0, "Account 1", "query_id of account 1"))
major_queries.append(MajorQuery(1, "Account 2", "query_id of account 2"))
major_queries.append(MajorQuery(2, "Account 3", "query_id of account 3"))
'''

## Installation
You can download the [repository](https://github.com/glad-tidings/MajorBot/) by cloning it to your system and installing the necessary dependencies:
Linux:
```bash
pip3 install -r requirements.txt
python3 Major.py
```
Windows:
```bash
pip install -r requirements.txt
python Major.py
```
