from app.workflow import workflow
import os


if __name__ == '__main__':
    print('START')

    app = workflow.compile()

    input = {'question': 'PM of India'}

    for output in app.stream(input):
        for key, value in output.items():
            print(f"Finished running: {key}:")
    print(value["generation"])