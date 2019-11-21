import requests
import json

# file_name = "test-users.csv"
file_name = "users.csv"
url = "http://10.21.25.228:9090/api/v1/users"

headers = {
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjdmMjBiNjA3NjE1OGMxZGJlNzU4ZTUzYmU1YzM1Y2JmOTY3OTkwNzVmOTI0ZTMwOGU2M2FmYjhjNDgwMjM1NTc0ODk0YWZiNjZkNDQ0Mjc0In0.eyJhdWQiOiIxIiwianRpIjoiN2YyMGI2MDc2MTU4YzFkYmU3NThlNTNiZTVjMzVjYmY5Njc5OTA3NWY5MjRlMzA4ZTYzYWZiOGM0ODAyMzU1NzQ4OTRhZmI2NmQ0NDQyNzQiLCJpYXQiOjE1NTExNzYxOTQsIm5iZiI6MTU1MTE3NjE5NCwiZXhwIjoxNTgyNzEyMTk0LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.MtA-GscJScXzw_IK9lh6tH4lCIV9yWoEYsQ79Av2cpB6Nj2H8zUbNsU74bNGspJpP5MiWEO67n2FXmuVNnIRUnqJF9q8rKdCNDUQmWAlUFbCJ2NzF0kJG0o9K_CmrGs21QVv64IomFU8x26yjp8GiMSH2svH8x-amm2OXkEUg-_pqkJRoX4LnNXVz0Q7UcwhxoDwPzy-b6sxxLxG9aPDNBdTQbNSsUM0mq5SzZhlmO0XfOemDqcvKjYp6wITjZuJLB9ISLzYtIvbg8gyQ4V0PTUZP_keHX181iSWDXNtxorySX9v8FNgTbUOOYy55ZTTl-67iBMSmiDTGVjcJhFEQ1OQQAnlMiJY6xlgYLU9pkyoTg5L8h_c356nRD8mhaw8pnhKgLL7OaUAJw52ckBQlOYq9LV57oeoAfDGfWAMZhpxCAnIFyj_uvU02fvBcSAunwUckYawW5eSrzc4MgsyXgSlhtSZptY2GA3ITs4rO3yUX2G2mvIJdYoWA68SuGXzYbVjV-8QOeeR2mEYFdn5K1N6qvEgZivkE9KQNKmKZjfkqX2-YcqiExdBGTlwwkSA70O_cV4XaeprFQ5RrlfAvA_BK-69E3eAJrr7PVk1aoEbVgHjxTLezqonmDV2HbhkvLTzEo9mq1-7znNSHyDS5gOcGmfNwOyOJ3Rhi1UItbA",
    'Accept': "application/json",
    'Content-Type': "application/json",
    }

payload = {
    'first_name': '',
    'username': '',
    'password': '123456',
    'password_confirmation': '123456',
    'activated': True,
    'groups': 2,
    'email': '',
    'notes': ''
    }

user_list = []
with open(file_name) as f:
    f.readline()
    for line in f.readlines():
        user_list.append(line.rstrip().split(','))

for user in user_list:
    payload['first_name'] = user[1]
    payload['username'] = user[3]
    payload['email'] = user[2]
    payload['notes'] = user[0]
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    if response.json()['status'] != 'success':
        print(payload)
        print(response.text)
