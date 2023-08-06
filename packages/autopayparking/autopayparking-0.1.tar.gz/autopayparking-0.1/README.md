# AutoPayParking
Pay and automatically renew PayByPhone parking using CLI.

### Installation
```bash
pip install autopayparking
```

### Usage
Omit `--renew` if you do not want to automatically renew parking:
```bash
autopayparking --location-number 123456 --duration 60 --renew --cc-name "Michael Jordan" --cc-number 1234567890 --cc-expiration 0125 --cc-cvv 1234 --cc-zip-code 12345 --email hello@example.com
```
