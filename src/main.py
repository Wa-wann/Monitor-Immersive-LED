from src.led_values_manager import LedValuesManager


def main():
    # TODO : @Kabroc you might have to test to modify ledValuesManager parameters
    ledValuesManager = LedValuesManager(1920, 1080, 10, 20)
    ledValuesManager.run()


if __name__ == "__main__":
    main()
