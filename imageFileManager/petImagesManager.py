import os

storage_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/storage/pet')

'''pet fotograflarını locale kaydeder'''
def pet_image_saving_directory(animal_name: str, image, user_id, time):
    os.chdir(storage_folder)
    if not os.path.exists(animal_name):
        os.mkdir(animal_name)
        print('done')
    os.chdir(animal_name)
    image.save('{}_{}_{}.jpg'.format(animal_name, user_id, time))
    return {'image_path': os.path.join(os.getcwd(), '{}_{}_{}.jpg'.format(animal_name, user_id, time))}
