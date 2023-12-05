import RPi.GPIO as GPIO
from openai import OpenAI
from secret import API_KEY
import json
import time


from colorama import Fore
import os

client = OpenAI(
  api_key=API_KEY,
)

#raspberry pi gpio
fanpin = 12            # BCM pin used to drive PWM fan
redPin   = 11
greenPin = 13
bluePin  = 15

PWM_FREQ = 25           # [kHz] 25kHz for Noctua PWM control

FAN_HIGH = 100
FAN_OFF = 0

RED = None
GREEN = None
BLUE = None
FAN = None

# action functions
def set_fan_speed(fan_speed):
    print()
    print(f" * fan speed {fan_speed} *")
    FAN.ChangeDutyCycle(fan_speed)
    return {"success": True}


def set_Living_Room_RGB_LED_Color(r,g,b):
    print()
    print(f"SET COLOR: * r: {r} g: {g} b:{b} *")
    RED.ChangeDutyCycle(r)
    GREEN.ChangeDutyCycle(g)
    BLUE.ChangeDutyCycle(b)
    return {"success": True}


def configureGPIO():
    global RED, GREEN, BLUE, FAN
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    #  confiugre pins
    GPIO.setup(fanpin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(redPin, GPIO.OUT)
    GPIO.setup(greenPin, GPIO.OUT)
    GPIO.setup(bluePin, GPIO.OUT)

    FAN = GPIO.PWM(fanpin, PWM_FREQ)

    # LED configure
    Freq = 100
    RED = GPIO.PWM(redPin, Freq)
    GREEN = GPIO.PWM(greenPin, Freq)
    BLUE = GPIO.PWM(bluePin, Freq)

    FAN.start(1)
    RED.start(1)
    GREEN.start(1)
    BLUE.start(1)

    set_fan_speed(FAN_OFF)
    set_Living_Room_RGB_LED_Color(0, 0, 0)


def main():
    
    print("configure PIN")
    configureGPIO()

    os.system('cls' if os.name == 'nt' else 'clear')

    thread = client.beta.threads.create()
    assistant_id = "asst_faISyeBqmKCrSPcYLj5sOD0R"

    while True:
        
        # get user message
        userMessage = input("User|> ")

        # add user message
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=userMessage
        )

        # run user message
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        run_id = run.id


        run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run_id
        )

        while run_status.status != 'completed':

                    # wait for run status
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run_id
            )
            time.sleep(2.5)

            if run_status.status == "requires_action":
                
                # pull function attributes
                tool_call_id = run_status.required_action.submit_tool_outputs.tool_calls[0]
                function_name = run_status.required_action.submit_tool_outputs.tool_calls[0].function.name
                function_arguments = json.loads(run_status.required_action.submit_tool_outputs.tool_calls[0].function.arguments)
                
                # run functions
                function_response = {"success": False}
                if function_name == "set_fan_speed":
                    function_response = set_fan_speed(function_arguments["fan_speed"])
                
                if function_name == "set_Living_Room_RGB_LED_Color":
                    function_response = set_Living_Room_RGB_LED_Color(function_arguments["red"], function_arguments["green"], function_arguments["blue"])
                
                #submit function output
                run_status = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run_id,
                    tool_outputs=[
                        {
                            "tool_call_id": tool_call_id.id,
                            "output": str(function_response),
                        }
                    ]
                )
        
        messages = client.beta.threads.messages.list(
        thread_id=thread.id)
        
        # Output system message
        print(f"\nIOT-Manager:\n{Fore.LIGHTGREEN_EX}", end="")
        print(messages.data[0].content[0].text.value)
        print(f"{Fore.WHITE}")


if __name__ == "__main__":
    
    
    
    try:
        main()
    except KeyboardInterrupt:
        print("EXCITING")
    finally:
        print(f"{Fore.WHITE}")