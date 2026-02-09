//changed dataDir path to DataAnalysis

#include "constants.h"

#include <string>

using namespace std;
std::string mnt = "/home/lilyg/TrinityDemonstrator/";
std::string dataDir = "/home/lilyg/TrinityDemonstrator/DataAnalysis/";
std::string outDir = "/home/lilyg/TrinityDemonstrator/DataAnalysis/DataSummary/Output/";
//total number of pixels 
const int maxCh = 256;
// 2 min per bin?
const int binLen = 120;

//                                  0                                                   1                                                           2                                                       3                                                           4                                    5                                       6                                       7                              8                                      9                                   10                                          11                                      12                                  13
const vector<string> hTitles = {"Average Amplitude of HLED Events 44V [ADC Counts]","Average Amplitude of HLED Events normalized to median 44V","Average Amplitude of HLED Events 41.5V [ADC Counts]","Average Amplitude of HLED Events normalized to median 41.5V","Average Pedestal 44V [ADC Counts]","Average Pedestal RMS 44V [ADC Counts]","Average Amplitude 44V [ADC Counts]","Average Charge 44V [ADC Counts]","Average Peak Time 44V [Time bins]","Average Pedestal 41.5V [ADC Counts]","Average Pedestal RMS 41.5V [ADC Counts]","Average Amplitude 41.5V [ADC Counts]","Average Charge 41.5V [ADC Counts]","Average Peak Time 41.5V [Time bins]"};
//                                  0                                                   1                                                   2                                                       3                                                   4                                   5                                       6                                   7                                  8                                    9                                       10                                      11                                      12                                  13
const vector<string> dTitles = {"Average Amplitude of HLED Events 44V [ADC Counts]","Standard Deviation of Amplitude Distribution 44V","Average Amplitude of HLED Events 41.5V [ADC Counts]","Standard Deviation of Amplitude Distribution 41.5V","Average Pedestal 44V [ADC Counts]","Average Pedestal RMS 44V [ADC Counts]","Average Amplitude 44V [ADC Counts]","Average Charge 44V [ADC Counts]","Average Peak Time 44V [Time bins]","Average Pedestal 41.5V [ADC Counts]","Average Pedestal RMS 41.5V [ADC Counts]","Average Amplitude 41.5V [ADC Counts]","Average Charge 41.5V [ADC Counts]","Average Peak Time 41.5V [Time bins]"};

// const vector<string> hTitles = {"Average Amplitude of HLED Events [ADC Counts]","Average Amplitude of HLED Events normalized to median","Average Pedestal [ADC Counts]","Average Pedestal RMS [ADC Counts]","Average Amplitude [ADC Counts]","Average Charge [ADC Counts]","Average Peak Time [Time bins]"};
// const vector<string> dTitles = {"Average Amplitude of HLED Events [ADC Counts]","Standard Deviation of Amplitude Distribution","Average Pedestal [ADC Counts]","Average Pedestal RMS [ADC Counts]","Average Amplitude [ADC Counts]","Average Charge [ADC Counts]","Average Peak Time [Time bins]"};

// 7 vals - need to change for dp - just repeat these? -- avgVales for hledMean etc?
// const vector<double> avgVals = {1100,0.15,3783,26,87,229,249};
const vector<double> avgVals = {1100,0.15,3783,26,87,229,249,1100,0.15,3783,26,87,229,249};

const vector<int> MUSICmap = {3,2,11,10,19,18,27,26,7,6,15,14,23,22,31,30,1,0,9,8,17,16,25,24,5,4,13,12,21,20,29,28};
const string trStr = "200000ffff250300"; //first 16 bits of 18 bit hex command for setting trigger threshold, last 2 bits are the threshold value