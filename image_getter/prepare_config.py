import csv
from faker import Faker


Faker.seed(0)
fake = Faker()

counter = 0
image_urls = set()
image_entries = []


if __name__ == '__main__':
    filename = 'config.csv' 
    with open(filename, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='\n')
        while counter < 1000:
            image_url = fake.file_name(category='image')
            if image_url not in image_urls:
                image_urls.add(image_url)
                counter += 1
            display_counter = str(fake.random_int(1, 10))
            categories = [fake.word() for _ in range(fake.random_int(1, 10))]
            writer.writerow([image_url, display_counter, *categories])
