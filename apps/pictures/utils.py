import os

def get_order_image_path(order, image_group, relative_path, renamed_filename):
    # Replace spaces in the order address with underscores
    order_address = order.address.replace(' ', '_')

    # Correctly format the group count as a two-digit number
    group_count = image_group.order.orderimagegroup_set.filter(created_by_view='PhotographerImageUploadView').count()

    # Ensure the group count is padded to two digits
    group_dir = f'{order_address}{group_count:02d}'

    # Fallback if relative_path is None
    if not relative_path:
        relative_path = renamed_filename
    else:
        relative_path = os.path.join(os.path.basename(os.path.dirname(relative_path)), renamed_filename)

    # Build the base directory using the desired format
    base_dir = f'{order_address}/{group_dir}'

    # Concatenate the base directory with the relative file path
    path = os.path.join(base_dir, relative_path)

    return path


def rename_file(image_group, filename):
    # Get the file extension
    extension = filename.split('.')[-1]

    # Generate the new filename based on the current count of images in the group
    new_filename = f'Spotlight{image_group.images.count() + 1:02d}.{extension}'

    return new_filename
