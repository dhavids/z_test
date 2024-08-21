#include <iostream>
#include <iomanip>

using namespace std;

struct Time {
    int hours;
    int minutes;
    int seconds;
};

bool isValidTime(Time t) {
    return t.minutes >= 0 && t.minutes < 60 &&
           t.seconds >= 0 && t.seconds < 60;
}

void computeTimeDifference(Time start, Time end, Time *difference) {
    // Convert times to seconds
    int startTotalSeconds = start.hours * 3600 + start.minutes * 60 + start.seconds;
    int endTotalSeconds = end.hours * 3600 + end.minutes * 60 + end.seconds;

    // Calculate difference (might be negative if end time is earlier so take absolute value)
    int diffSeconds = abs(endTotalSeconds - startTotalSeconds);

    // Convert back to Time struct
    difference->hours = diffSeconds / 3600;
    difference->minutes = (diffSeconds % 3600) / 60;
    difference->seconds = diffSeconds % 60;
}

int main() {
    Time t1, t2, difference;

    do {
        cout << "Enter start time (HH MM SS): ";
        cin >> t1.hours >> t1.minutes >> t1.seconds;
    } while (!isValidTime(t1));

    do {
        cout << "Enter end time (HH MM SS): ";
        cin >> t2.hours >> t2.minutes >> t2.seconds;
    } while (!isValidTime(t2));

    computeTimeDifference(t1, t2, &difference);

    cout << endl << "TIME DIFFERENCE: " 
         << setfill('0') << setw(2) << t1.hours << ":" 
         << setw(2) << t1.minutes << ":"
         << setw(2) << t1.seconds << " - "
         << setw(2) << t2.hours << ":" 
         << setw(2) << t2.minutes << ":"
         << setw(2) << t2.seconds << " = "
         << setw(2) << difference.hours << ":" 
         << setw(2) << difference.minutes << ":"
         << setw(2) << difference.seconds << endl;

    return 0;
}