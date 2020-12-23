# Useless Box

This is an useless application that has an useless logic, which I decided to develop only to improve my skills.

#### Workflow
The box follows this useless workflow:

1. Produce: generate a 20 digits alphanumerical string
2. Consume: sum all of the numbers in the string
3. Log: Log the results in a file

## Dependency

The application requires [docker-compose](https://docs.docker.com/compose/install/).

## Usage
As easy as an useless box:
```shell
make run
```
On runtime, or after, in another terminal, check the log file with:
```shell
tail -f ./consumer/log.txt
```

## Improvements
Since the only reason for this project is improving my skills, feel free to drop a suggestion/review.
