import csv


def save_telemetry(operation, cluster, chunk_size, data):
    with open(f'results/{cluster}-{operation}{chunk_size}.csv', 'w', newline='') as file:
        fieldnames = ['Operation', 'Rows', 'Speed']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
