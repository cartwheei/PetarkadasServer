import os

storage_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/storage/pet')


# pet fotograflarını kaydeder
def pet_image_saving_directory(animal_name: str, image, user_id):
    os.chdir(storage_folder)
    if not os.path.exists(animal_name):
        os.mkdir(animal_name)
        print('done')
    os.chdir(animal_name)
    image.save('test{}.jpg'.format(user_id))
    return {'image_path': os.path.join(os.getcwd(), '{}{}.jpg'.format(animal_name, user_id))}
