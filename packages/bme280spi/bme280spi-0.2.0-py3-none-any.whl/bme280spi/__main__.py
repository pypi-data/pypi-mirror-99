import argparse

from bme280spi.main import BME280


def main() -> None:
    """Module entrypoint"""
    parser = argparse.ArgumentParser(description='BME280 sensor communication module.')

    parser.add_argument(
        '-b',
        '--bus',
        dest='spi_bus',
        action='store',
        type=int,
        default=0,
        help='spi bus (default: 0)',
    )
    parser.add_argument(
        '-d',
        '--dev',
        dest='spi_dev',
        action='store',
        type=int,
        default=0,
        help='spi device (default: 0)',
    )
    args = parser.parse_args()
    device = BME280(args.spi_bus, args.spi_dev)
    print(
        (
            '{{"bus": {0}, "device": {1}, "temperature": {2}, '
            '"humidity": {3}, "pressure": {4}}}'
        ).format(
            args.spi_bus,
            args.spi_dev,
            device.temperature,
            device.humidity,
            device.pressure,
        )
    )


if __name__ == '__main__':
    main()
