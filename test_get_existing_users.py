from add_to_loops import check_user_existence_by_email

if __name__ == "__main__":
    email = "benjamin.shafii@gmail.com"
    exists = check_user_existence_by_email(email)
    if exists:
        print(f"User with email {email} exists.")
    else:
        print(f"User with email {email} does not exist.")