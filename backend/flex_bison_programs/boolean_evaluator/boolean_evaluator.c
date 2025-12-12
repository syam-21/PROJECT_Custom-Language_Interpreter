#include <stdio.h>
#include <ctype.h>
#include <string.h>

const char *p;  // global pointer to input string

// Forward declarations
int expr();
int term();
int factor();

// Parse factor: NUMBER or !factor or (expr)
int factor() {
    while (*p == ' ') p++;  // skip spaces

    if (*p == '!') {
        p++;
        return !factor();
    }
    else if (*p == '(') {
        p++;
        int val = expr();
        if (*p == ')') p++;
        return val;
    }
    else if (*p == '0' || *p == '1') {
        int val = *p - '0';
        p++;
        return val;
    }
    return 0; // default
}

// Parse term: factor && factor ...
int term() {
    int val = factor();
    while (1) {
        while (*p == ' ') p++;
        if (p[0] == '&' && p[1] == '&') {
            p += 2;
            val = val && factor();
        } else {
            break;
        }
    }
    return val;
}

// Parse expr: term || term ...
int expr() {
    int val = term();
    while (1) {
        while (*p == ' ') p++;
        if (p[0] == '|' && p[1] == '|') {
            p += 2;
            val = val || term();
        } else {
            break;
        }
    }
    return val;
}

int evaluate(const char *s) {
    p = s;
    return expr();
}

int main() {
    char input[256];

    // No interactive prompt here, just process lines from stdin
    while (fgets(input, sizeof(input), stdin)) {
        // remove newline
        input[strcspn(input, "\n")] = 0;

        // Skip empty lines or just spaces
        if (strlen(input) == 0 || strspn(input, " ") == strlen(input)) {
            continue;
        }

        int result = evaluate(input);
        printf("%d\n", result);
    }

    return 0;
}
