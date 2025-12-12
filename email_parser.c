#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// Check if email is valid
bool isValidEmail(const char *email) {
    if (strchr(email, '@') == NULL) return false;
    if (strchr(email, '.') == NULL) return false;
    if (email[0] == '@') return false;
    return true;
}

// Check if email belongs to DIU
bool isDIUEmail(const char *email) {
    const char *domain = "@diu.edu.bd";
    int lenEmail = strlen(email);
    int lenDomain = strlen(domain);
    if (lenEmail < lenDomain) return false;
    return strcmp(email + (lenEmail - lenDomain), domain) == 0;
}

// Check if email is university email (.edu or .edu.bd)
bool isUniversityEmail(const char *email) {
    int len = strlen(email);
    if (len >= 4 && strcmp(email + len - 4, ".edu") == 0) return true;
    if (len >= 7 && strcmp(email + len - 7, ".edu.bd") == 0) return true;
    return false;
}

int main() {
    char emails[][50] = {
        "student123@diu.edu.bd",
        "teacher.cse@diu.edu.bd",
        "john.doe@gmail.com",
        "invalidemail.com",
        "@diu.edu.bd"
    };

    int n = sizeof(emails) / sizeof(emails[0]);

    for (int i = 0; i < n; i++) {
        bool valid = isValidEmail(emails[i]);
        bool diu = isDIUEmail(emails[i]);
        bool uni = isUniversityEmail(emails[i]);

        char status[30];
        if (!valid) strcpy(status, "Invalid");
        else if (diu) strcpy(status, "Valid (University)");
        else strcpy(status, "Valid (Non-University)");

        printf("Email: %s | Status: %s | Is University Mail (.edu): %s\n",
               emails[i],
               status,
               uni ? "Yes" : "No");
    }

    return 0;
}