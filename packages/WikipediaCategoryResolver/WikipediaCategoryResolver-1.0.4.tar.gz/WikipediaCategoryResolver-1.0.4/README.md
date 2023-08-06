# Entity Recognition using Wikipedia API
This project uses Wikipedia's API to search a given keyword in the database. It resolves the keyword to its categories. A relevant snippet/ brief description about the subject is also returned.

## Setup
`pip install WikipediaCategoryResolver`

## Usage
```
from WikipediaCategoryResolver import Wiki
wiki = Wiki()
wiki.get_category('AWS')  #Example
```