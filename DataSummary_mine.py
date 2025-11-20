#include "DataSummary.h"

#include "constants.h"
#include "rootils.h"
#include "DtStruct.h"

#include <TROOT.h>
#include <TTree.h>
#include <TFile.h>
#include <TMath.h>
#include <TH1.h>
#include <TH2.h>
#include <TF1.h>
#include <TGraph.h>
#include <TGraphErrors.h>
#include <TCanvas.h>
#include <TLine.h>
#include <TStyle.h>
#include <TPaveStats.h>
#include <TPaveText.h>
#include <TLegend.h>

// I added
#include <IEvent.h>
#include <TTree.h>
#include <IUtilities.h>
#include <ISiPM.h>
#include <TFile.h>
//

#include <Event.h>
#include <Pulse.h>

#include <dirent.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>


using namespace std;

// DataSummary() def
DataSummary::DataSummary(char* dateStr){
    avgEv = 0;
    ampDist = 0;
    hledMean = 0;
    hledNMean = 0;
    pedMean = 0;
    pedRMSMean = 0;
    ampMean = 0;
    qMean = 0;
    ptMean = 0;
    psfSigma = 0;
    trTh = vector<vector<int>>();
    //
    hledEv = vector<DtStruct>();
    testEv = vector<DtStruct>();
    //
    pixMeans = vector<vector<Double_t>>(7,vector<Double_t>(maxCh,0.0));
    meanPedRMS = vector<Double_t>(16,0.0);
    fConvolutedFit = new TF1();
    camera = new TH2F();
    ddt = new TH2F();
    addt = new TH2F();
    trig = new TH1F();
    misc1 = new TH1F();
    misc2 = new TGraph();
    lin = new TLine();
    leg = new TLegend();
    pt = new TPaveText();
    t_disp = new TCanvas("Display","DataSummary",2500,1000);
    // initialize isData as false
    isData = false;

    // dataDir = "/storage/osg-otte1/shared/TrinityDemonstrator/DataAnalysis/"
    string evStr = Form("%s%s/MergedData/Output/",dataDir.c_str(),dateStr);
    string logDir = Form("%s%s/LOGS/rc.log",dataDir.c_str(),dateStr);

    // Readv() called for  MergedData/Output/yyyymmdd files
    ReadEv(evStr);

    // isData (boolean) called
    // if false (?)
    if(isData){
        // NUMBER OF EVENTS PLOT
        FillTrig();
        ReadTrThresholds(logDir);
        // ? for rc./yyyymmdd
    }
    // end isData call
}
// end DataSummary() def

// PER NIGHT
// ReadEv() called for night yyyymmdd
void DataSummary::ReadEv(string readStr){
    // tree = pointer to TTree object
    TTree *tree;
    // ev = pointer to Event object
    Event *ev;
    // initialize countF 
    int countF = 0;
    // load in files
    DIR *dir;
    struct dirent *ent;
    // PER FILE OF NIGHT
    if((dir = opendir(readStr.c_str())) != NULL){
        while((ent = readdir(dir)) != NULL){
            string fileStr = Form("%s%s",readStr.c_str(),ent->d_name);
            if(fileStr.substr(fileStr.find_last_of(".")+1) == "root"){
                cout << "Loading file: " << fileStr << endl;
                TFile *f0 = TFile::Open(fileStr.c_str());
                if(!f0){
                    cout << "File is a zombie...skipping" << endl;
                    continue;
                }
            // TESTING FOR TEST EVENTS
                // get test events
                tree = (TTree*)f0->Get("Test");
                //create new Event object (ExACT type)
                ev = new Event();
                // sets branch of tree to "Events"
                tree->SetBranchAddress("Events", &ev);
                // get number entires in current file
                int nEntries = tree->GetEntries();
                // if current file empty: skip
                if(nEntries == 0){
                    cout << "File has no data in the \"Test\" branch...skipping" << endl;
                    delete ev;
                    delete tree;
                    f0->TFile::Close();
                    continue;
                } 
                // if file not empty:
                // add to countF incrementally
                countF++;
                cout << "\"Test\" Events: " << nEntries << endl;
                // PER EVENT IN FILE
                // iterate through each event in file
                for(int evCount = 0; evCount < nEntries; evCount++){
                    // get tree entry associated w event number evCount
                    tree->GetEntry(evCount);
                    // looks for HLED events: 
                    // if((ampVal/maxCh) < 350) -> true
                    if(isHLED(ev)){
                        // adds event to testEv vector
                        AddTestEv(ev);
                        // testEv.push_back(DtStruct(false));
                        // testEv[testEv.size()-1].data[0] += maxCurrent
                        // testEv[testEv.size()-1].data[1] += BVAvg
                    }
                    // if ((ampVal/maxCh) > 350) -> false
                    else{
                        // add event to hledEv vector
                        AddHLEDEv(ev);
                    }
                }
                delete ev;
                delete tree;

            // TESTING FOR HLED EVENTS
                tree = (TTree*)f0->Get("HLED");
                ev = new Event();
                tree->SetBranchAddress("Events", &ev);
                nEntries = tree->GetEntries();
                if(nEntries == 0){
                    cout << "File has no data in the \"HLED\" branch...skipping" << endl;
                    continue;
                }
                cout << "\"HLED\" Events: " << nEntries << endl;
                // iterate through each event in file
                // AGAIN PER EVENT IN FILE
                for(int evCount = 0; evCount < nEntries; evCount++){
                    tree->GetEntry(evCount);
                    // look for HLED events
                    if(isHLED(ev)){
                        AddTestEv(ev);
                    }
                    else{
                        AddHLEDEv(ev);
                    }
                }
                delete ev;
                delete tree;
                // close file
                f0->TFile::Close();
            }
        }
    }
    // BACK TO PER NIGHT
    if(countF != 0){
        //calls FillTrig() and ReadTrThresholds(logDir)
        isData = true;
        int hledEnt = hledEv.size();
        int testEnt = testEv.size();
        for(int i = 0; i < maxCh; i++){ //maxCH? pixMeans = vector<vector<Double_t>>(7,vector<Double_t>(maxCh,0.0));
            for(int j = 0; j < 2; j++){
                // mean pixels for HLED entries
                pixMeans[j][i] /= hledEnt;
            }
            for(int j = 2; j < 7; j++){
                // mean pixels for Test entries
                pixMeans[j][i] /= testEnt;
            }
        }
        for(int i = 0; i < 16; i++){
            // meal pedestal RMS for test entries
            meanPedRMS[i] /= testEnt;
        }
        Double_t medianLED = Median(pixMeans[1]);
        for(int i = 0; i < maxCh; i++){
            pixMeans[1][i] /= medianLED;
        }
        sort(testEv.begin(),testEv.end());
        sort(hledEv.begin(),hledEv.end());
        avgEv = testEnt/countF;
        hledMean = accumulate(pixMeans[0].begin(),pixMeans[0].end(),0.0)/maxCh;
        hledNMean = accumulate(pixMeans[1].begin(),pixMeans[1].end(),0.0)/maxCh;
        pedMean = accumulate(pixMeans[2].begin(),pixMeans[2].end(),0.0)/maxCh;
        pedRMSMean = accumulate(pixMeans[3].begin(),pixMeans[3].end(),0.0)/maxCh;
        ampMean = accumulate(pixMeans[4].begin(),pixMeans[4].end(),0.0)/maxCh;
        // q = ?
        qMean = accumulate(pixMeans[5].begin(),pixMeans[5].end(),0.0)/maxCh;
        // pt = ?
        ptMean = accumulate(pixMeans[6].begin(),pixMeans[6].end(),0.0)/maxCh;
    }
}
// end ReadEv() call

// isHLED def
// boolean test for HLED events
bool DataSummary::isHLED(Event *&ev){
    Pulse *pulse;
    double ampVal = 0;
    for(int i = 0; i < maxCh; i++){
        pulse = new Pulse(ev->GetSignalValue(i));
        ampVal += pulse->GetAmplitude();
        delete pulse;
    }
    if((ampVal/maxCh) < 350){
        // HLED
        return true;
    }
    // Not HLED
    return false;
}

// AddTestEv def
void DataSummary::AddTestEv(Event *&ev){
    // data = vector<Double_t>(5,0.0);
    testEv.push_back(DtStruct(false));
    // get TB time
    testEv[testEv.size()-1].time = ev->GetTBTime()*1e-8;
    Pulse *pulse;
    for(int i = 0; i < maxCh; i++){
        // get pulse signal value
        pulse = new Pulse(ev->GetSignalValue(i));
        // add values to pixMeans
        pixMeans[2][i] += pulse->GetPedestal();
        pixMeans[3][i] += pulse->GetPedestalRMS();
        pixMeans[4][i] += pulse->GetAmplitude();
        pixMeans[5][i] += pulse->GetCharge();
        pixMeans[6][i] += pulse->GetTimePeak();

        // add data to testEv vector
        testEv[testEv.size()-1].data[0] += pulse->GetPedestal();
        testEv[testEv.size()-1].data[1] += pulse->GetPedestalRMS();
        testEv[testEv.size()-1].data[2] += pulse->GetAmplitude();
        testEv[testEv.size()-1].data[3] += pulse->GetCharge();
        testEv[testEv.size()-1].data[4] += pulse->GetTimePeak();
        
        delete pulse;
    }
    // avg testEvs (?)
    testEv[testEv.size()-1].Avg();
    // for i of 0-4
    for(int i = 0; i < 4; i++){
    // what is i?
        // for j of 0-4
        for(int j = 0; j < 4; j++){
        // what is j?
            // for k of 8-9
            for(int k = 8; k < 9; k++){
            // what is k?
                // i = 0,1,2,3,4
                // j = 0,1,2,3,4
                // k = 8,9
                // get signal value for i*64 + j + k*4
                pulse = new Pulse(ev->GetSignalValue(i*64+j+k*4));
                // what is this value?
                // mean pedestal rms for 4*i + j
                meanPedRMS[4*i+j] += pulse->GetPedestalRMS();
                // what is this value?
                delete pulse;
            }
        }
    }
    // end all for loops

    // MUSIC section
    int MUSICpos = MUSICmap[(ev->GetROIMusicID())[0]];
    testEv[testEv.size()-1].pTrig = MUSICpos*8;
    Double_t ampMax = 0;
    for(int i = 0; i < 8; i++){
        pulse = new Pulse(ev->GetSignalValue(MUSICpos*8 + i));
        // if pulse amp > max amp (=0?)
        if(pulse->GetAmplitude() > ampMax){
            testEv[testEv.size()-1].pTrig = MUSICpos*8 + i;
            //max amplitude
            ampMax = pulse->GetAmplitude();
        }
        delete pulse;
    }
    // end "for i" loop
}
// end AddTestEv def

// AddHLEDEv def
void DataSummary::AddHLEDEv(Event *&ev){
    vector<Double_t> amps(maxCh);
    TH1 *ledDist = new TH1F("hledDist","Amplitudes normalized to camera median",100,0,2);
    // data = vector<Double_t>(2,0.0)
    hledEv.push_back(DtStruct(true));
    // get TB time
    hledEv[hledEv.size()-1].time = ev->GetTBTime()*1e-8;
    Pulse *pulse;
    for(int i = 0; i < maxCh; i++){
        // get signal value
        pulse = new Pulse(ev->GetSignalValue(i));
        
        // add amplitudes to pixMeans
        pixMeans[0][i] += pulse->GetAmplitude();
        pixMeans[1][i] += pulse->GetAmplitude();

        // add amplitudes to amps
        amps[i] = pulse->GetAmplitude();

        //adds data to hledEv vector
        hledEv[hledEv.size()-1].data[0] += pulse->GetAmplitude();
        
        delete pulse;
    }
    // median amp
    Double_t medianLED = Median(amps);
    for(int i = 0; i < maxCh; i++){
        ledDist->Fill(amps[i]/medianLED);
    }
    // avg hledEv
    hledEv[hledEv.size()-1].Avg();
    // get standard dev for hledEv
    hledEv[hledEv.size()-1].data[1] =  ledDist->GetStdDev();
    delete ledDist;
}
// end AddHLEDEv def

// ReadTrThresholds() def
void DataSummary::ReadTrThresholds(string readStr){
    ifstream logFile(readStr);
    string line, prevLine;
    bool found = false;
    if(!logFile.is_open()){
        cout << "Error opening RC log file" << endl;
    }
    vector<int> tempTr = {0,0};
    while(getline(logFile,line)){
        if(found){
            string trSetTime = line.substr(13,13);
            for(char& c : trSetTime){
                if(c=='_'){
                    c = 'T';
                }
            }
            time_t unixThresTime=convertToUnixTime("20"+trSetTime,0);
            tempTr[0] = (int)unixThresTime;
            trTh.push_back(tempTr);
            tempTr = {0,0};
            found = false;
        }
        size_t pos = line.find(trStr);
        if(pos != string::npos){
            string trValHex = line.substr(51,2);
            int trVal = stoi(trValHex,nullptr,16);
            tempTr[1] = trVal;
            found = true;
            prevLine = line;
        }
    }
    logFile.close();
}

// FillCamera() def
void DataSummary::FillCamera(int dp){
    if(camera){delete camera;}
    // constants.cpp: const vector<string> hTitles = {"Average Amplitude of HLED Events [ADC Counts]","Average Amplitude of HLED Events normalized to median","Average Pedestal [ADC Counts]","Average Pedestal RMS [ADC Counts]","Average Amplitude [ADC Counts]","Average Charge [ADC Counts]","Average Peak Time [Time bins]"};
    camera = new TH2F("camera",hTitles[dp].c_str(),16,-0.5,15.5,16,-0.5,15.5);
    for(int i = 0; i < maxCh; i++){
        int nx, ny;
        FindBin(i,&nx,&ny);
        camera->SetBinContent(nx+1,ny+1,pixMeans[dp][i]);
    }
    camera->SetStats(0);
    //below finds histogram scale s.t. it includes 95% of pixels; purpose is to neglect outliers as opposed to just using min and max 
    vector<int> hRangeInd(2);
    vector<Double_t> valSort;
    for(auto i: pixMeans[dp]){
        valSort.push_back(i);
    }
    sort(valSort.begin(),valSort.end());
    int valSize = valSort.size();
    double valInc;
    if(valSize%2 != 0){
        hRangeInd = {valSize/2 - 1,valSize/2 + 1};
        valInc = 3;
    }
    else{
        hRangeInd = {valSize/2 - 1, valSize/2};
        valInc = 2;
    }
    while(valInc < valSize*0.95){
        Double_t up = valSort[hRangeInd[1]+1] - valSort[hRangeInd[1]];
        Double_t down = valSort[hRangeInd[0]] - valSort[hRangeInd[0]-1];
        if(up < down){
            ++hRangeInd[1];
            if(hRangeInd[1] == valSize - 1){
                hRangeInd[0] -= floor(valSize*0.95 - valInc);
                break;
            }
        }
        else{
            --hRangeInd[0];
            if(hRangeInd[0] == 0){
                hRangeInd[1] += floor(valSize*0.95 - valInc);
                break;
            }
        }
        ++valInc;
    }
    vector<Double_t> hRange = {valSort[hRangeInd[0]],valSort[hRangeInd[1]]};
    Double_t cushion = (hRange[1] - hRange[0]) * 0.05;
    camera->SetMinimum(hRange[0] - cushion);
    camera->SetMaximum(hRange[1] + cushion);
}

// FillDt() def
void DataSummary::FillDt(int dp){
    if(ddt){delete ddt;}
    if(addt){delete addt;}
    if(lin){delete lin;}
    vector<DtStruct> *thisVec;
    int dpt = dp - (dp >= 2)*2;
    if(dp<2){
        thisVec = &hledEv;
    }
    else{
        thisVec = &testEv;
    }
    //below finds y axis range s.t. it includes 99.9% of points; purpose is to neglect outliers as opposed to just using min and max 
    vector<int> yRangeInd(2);
    vector<Double_t> valSort;
    for(auto i: (*thisVec)){
        valSort.push_back(i.data[dpt]);
    }
    sort(valSort.begin(),valSort.end());
    int valSize = valSort.size();
    double valInc;
    if(valSize%2 != 0){
        yRangeInd = {valSize/2 - 1,valSize/2 + 1};
        valInc = 3;
    }
    else{
        yRangeInd = {valSize/2 - 1, valSize/2};
        valInc = 2;
    }
    while(valInc < valSize*0.999){
        Double_t up = valSort[yRangeInd[1]+1] - valSort[yRangeInd[1]];
        Double_t down = valSort[yRangeInd[0]] - valSort[yRangeInd[0]-1];
        if(up < down){
            ++yRangeInd[1];
            if(yRangeInd[1] == valSize - 1){
                yRangeInd[0] -= floor(valSize*0.999 - valInc);
                break;
            }
        }
        else{
            --yRangeInd[0];
            if(yRangeInd[0] == 0){
                yRangeInd[1] += floor(valSize*0.999 - valInc);
                break;
            }
        }
        ++valInc;
    }

    vector<Double_t> yRange = {valSort[yRangeInd[0]],valSort[yRangeInd[1]]};
    if(avgVals[dp] < yRange[0]){yRange[0] = avgVals[dp];}
    else if(avgVals[dp] > yRange[1]){yRange[1] = avgVals[dp];}
    Double_t yCushion = (yRange[1] - yRange[0]) * 0.05;
    // ddt = new TH2F();
    ddt = new TH2F("ddt", //Name
        // constants.cpp: const vector<string> dTitles = {"Average Amplitude of HLED Events [ADC Counts]","Standard Deviation of Amplitude Distribution","Average Pedestal [ADC Counts]","Average Pedestal RMS [ADC Counts]","Average Amplitude [ADC Counts]","Average Charge [ADC Counts]","Average Peak Time [Time bins]"};
        dTitles[dp].c_str(), //Title
        ((*thisVec).back().time - (*(*thisVec).begin()).time)/binLen, //number of bins on x axis
        (*(*thisVec).begin()).time, //x axis minimum
        (*thisVec).back().time, //x axis maximum
        1000, //number of bins on y axis
        yRange[0] - yCushion, //y axis minimum
        yRange[1] + yCushion //y axis maximum
    );
    // addt = new TH2F();
    addt = new TH2F("addt", //Name
        dTitles[dp].c_str(), //Title
        ((*thisVec).back().time - (*(*thisVec).begin()).time)/binLen, //number of bins on x axis
        (*(*thisVec).begin()).time, //x axis minimum
        (*thisVec).back().time, //x axis maximum
        1000, //number of bins on y axis
        yRange[0] - yCushion, //y axis minimum
        yRange[1] + yCushion //y axis maximum
    );
    int count = 0;
    Double_t runAvg = 0.0;
    for(auto i: (*thisVec)){
        runAvg += i.data[dpt];
        ++count;
        ddt->Fill(i.time,i.data[dpt]);
        addt->Fill(i.time,runAvg/count);
    }

    lin=new TLine((*(*thisVec).begin()).time, //x1
        avgVals[dp], //y1
        (*thisVec).back().time, //x2
        avgVals[dp] //y2
    );
}

// PlotAverages() def
// AVERAGES PLOTS (RIGHT SIDE)
void DataSummary::PlotAverages(int dp){
    if(leg){delete leg;}
    FillCamera(dp);
    FillDt(dp);
    if(t_disp){delete t_disp;}
    t_disp = new TCanvas("Display","DataSummary",2500,1000);
    t_disp->Divide(2,1);

    t_disp->cd(1);
    camera->Draw("colz");
    DrawMUSICBoundaries();
    t_disp->cd(1)->SetRightMargin(0.15);

    t_disp->cd(2);

    ddt->GetXaxis()->SetTimeDisplay(1);
    ddt->GetXaxis()->SetTimeFormat("%H:%M");
    ddt->GetXaxis()->SetTimeOffset(0,"gmt");
    ddt->GetXaxis()->SetTitle("UTC Time of Events [HH:MM]");
    ddt->SetStats(0);
    ddt->SetMarkerStyle(6);
    ddt->SetMarkerSize(6);
    ddt->SetMarkerColor(1);
    
    addt->SetStats(0);
    addt->SetMarkerStyle(6);
    addt->SetMarkerSize(6);
    addt->SetMarkerColor(6);

    lin->SetLineColor(kGreen);
    lin->SetLineColorAlpha(kGreen,0.6);
    lin->SetLineWidth(4);

    ddt->Draw("");
    addt->Draw("SAME");
    lin->Draw("SAME");

    leg = new TLegend(0.1,0.90,0.9,0.94);
    leg->SetNColumns(4);
    leg->AddEntry(ddt,"Data Points","p");
    leg->AddEntry(addt,"Running Avg","p");
    leg->AddEntry(lin,"Expected Avg","l");
    leg->Draw("SAME");
}

// FillTrig() def
// NUMBER OF EVENTS PLOT
void DataSummary::FillTrig(){
    if(trig){delete trig;}
    trig = new TH1F("trig", //Name
        "Number of Events", //Title
        (testEv.back().time - (*testEv.begin()).time)/binLen, //number of bins on x axis
        (*testEv.begin()).time, //x axis minimum
        testEv.back().time //x axis maximum
    );
    for(auto i: testEv){
        trig->Fill(i.time);
    }
    trig->GetXaxis()->SetTimeDisplay(1);
    trig->GetXaxis()->SetTimeFormat("%H:%M");
    trig->GetXaxis()->SetTimeOffset(0,"gmt");
    trig->GetXaxis()->SetTitle("UTC Time of Events [HH:MM]");
    trig->GetYaxis()->SetTitle("Events");
    trig->SetStats(0);
    trig->SetMarkerStyle(6);
    trig->SetMarkerSize(6);
    trig->SetMarkerColor(1);
}

// PlotTrig() def
// TRIGGER RATE PLOT
void DataSummary::PlotTrig(){
    if(t_disp){delete t_disp;}
    if(misc1){delete misc1;}
    t_disp = new TCanvas("Display","DataSummary",2500,1000);
    t_disp->Divide(2,1);
    t_disp->cd(1);
    t_disp->cd(1)->SetLogy();
    trig->SetAxisRange(1,4000,"Y");
    trig->Draw("P");
    t_disp->cd(2);
    misc1 = (TH1F*)trig->Clone("misc1");
    misc1->SetTitle("Trigger Rate [Events/s]");
    misc1->Scale((Double_t)1/binLen);
    misc1->SetAxisRange(0,35,"Y");
    misc1->GetYaxis()->SetTitle("Trigger rate [events/s]");
    misc1->Draw("P");
}

// PlotROIMusic() def
// HIGHEST AMPLITUDE PIXELS AND TRIGGERED MUSIC PLOT
void DataSummary::PlotROIMusic(){
    if(t_disp){delete t_disp;}
    if(camera){delete camera;}
    if(ddt){delete ddt;}

    camera = new TH2F("pixHeat","Highest Amplitude Pixels in Triggered Music [Counts]",16,-0.5,15.5,16,-0.5,15.5);
    ddt = new TH2F("musicHeat","Triggered Music [Counts]",8,-0.5,15.5,4,-0.5,15.5);
    for(auto i: testEv){
        int nx, ny;
		FindBin(i.pTrig,&nx,&ny);
		camera->Fill(nx,ny);
		ddt->Fill(nx,ny);
    }

    t_disp = new TCanvas("Display","DataSummary",2500,1000);
    t_disp->Divide(2,1);
    t_disp->cd(1);
	camera->Draw("colz");
	DrawMUSICBoundaries();
	camera->SetStats(0);
	t_disp->cd(1)->SetRightMargin(0.15);
	t_disp->cd(2);
	ddt->Draw("colz");
	DrawMUSICBoundaries();
	ddt->SetStats(0);
	t_disp->cd(2)->SetRightMargin(0.15);
}

// PlotFF() def
// DAILY AVG HLED AMPLITUDE DISTRIBUTION 
void DataSummary::PlotFF(){
    if(t_disp){delete t_disp;}
    if(misc1){delete misc1;}
    t_disp = new TCanvas("Display","DataSummary",1250,1000);
    misc1 = new TH1F("misc1", //Name
        "Distribution of Daily Average HLED Amplitude normalized to median", //Title
        150, //number of bins on x axis
        0, //x axis minimum
        1499 //x axis maximum
    );
    for(auto i: pixMeans[0]){
        misc1->Fill(i);
    }
    misc1->GetXaxis()->SetTitle("HLED signal amplitude normalized to median");
    misc1->GetYaxis()->SetTitle("Number of pixels");
    gStyle->SetOptStat(1100);
    t_disp->cd();
    misc1->Draw("hist");

    double stats[4];
    misc1->GetStats(stats);
    double tvar1 = (stats[0] > 0) ? (stats[2] / stats[0]) : 0.0;
    double tvar2 = (stats[0] > 0) ? (stats[3] / stats[0] - tvar1 * tvar1) : 0.0;
    double tvar3 = (tvar2 > 0) ? sqrt(tvar2) : 0.0;
    ampDist = tvar3 / tvar1;
}

// PlotHLED() def
// AVERAGE AMPLITUDE OF HLED EVENTS PLOT
void DataSummary::PlotHLED(){
    if(hledEv.size() > 0){PlotAverages(0);}
    else{
        t_disp->Clear();
    }
}

// PlotHLEDNorm() def
// NORMALIZED AVERAGE AMPLITUDE OF HLED EVENTS PLOT
void DataSummary::PlotHLEDNorm(){
    if(hledEv.size() > 0){PlotAverages(1);}
    else{
        t_disp->Clear();
    }
}

// PlotPedestal def
// AVERAGE PEDESSTAL PLOT
void DataSummary::PlotPedestal(){
    if(testEv.size() > 0){PlotAverages(2);}
    else{
        t_disp->Clear();
    }
}

//PlotPedestalRMS() def
// AVERGAE PREDESTAL RMS PLOT
void DataSummary::PlotPedestalRMS(){
    if(testEv.size() > 0){PlotAverages(3);}
    else{
        t_disp->Clear();
    }
}

// Plot Amplitude() def
// AVERAGE AMPLITUDE PLOT
void DataSummary::PlotAmplitude(){
    if(testEv.size() > 0){PlotAverages(4);}
    else{
        t_disp->Clear();
    }
}

// PlotCharge() def
// AVERGAE CHARGE PLOT
void DataSummary::PlotCharge(){
    if(testEv.size() > 0){PlotAverages(5);}
    else{
        t_disp->Clear();
    }
}

// PlotTimePeak() def 
// AVERAGE PEAK TIME PLOT
void DataSummary::PlotTimePeak(){
    if(testEv.size() > 0){PlotAverages(6);}
    else{
        t_disp->Clear();
    }
}

//PlotPSF() def
// AVG PEDESTAL RMS FOR PIXEL 8 PLOT (LAST ONE)
void DataSummary::PlotPSF(){
    if(t_disp){delete t_disp;}
    if(misc1){delete misc1;}
    if(misc2){delete misc2;}
    if(fConvolutedFit){delete fConvolutedFit;}
    if(pt){delete pt;}
    t_disp = new TCanvas("Display","DataSummary",1250,1000);
    misc1 = new TH1F("misc1", //Name
        "Average Pedestal RMS per Row for pixel column 8", //Title
        16, //number of bins on x axis
        0, //x axis minimum
        16 //x axis maximum
    );
    misc2 = new TGraph(16);

    for(int i = 0; i < 16; i ++){
        misc1->SetBinContent(i+1,meanPedRMS[i]);
        misc2->SetPoint(i,(i+0.5),meanPedRMS[i]);
    }

    fConvolutedFit = new TF1("fConvolutedFit", //Name
        ConvolutedRMSFunction, //Formula
        0, //x axis minimum
        16, //x axis maximum
        4 //number of free parameters (?)
    );
    // Initial parameters: [0]=offset, [1]=swing, [2]=mean (mu), [3]=sigma
    fConvolutedFit->SetParameters(20, 10, 8, 2); // Adjust initial parameters accordingly
    // Set limits for the parameters
    fConvolutedFit->SetParLimits(0, 0, 100); // Limits for offset
    fConvolutedFit->SetParLimits(1, 0, 100); // Limits for swing
    fConvolutedFit->SetParLimits(2, 0, 16); // Limits for mu
    fConvolutedFit->SetParLimits(3, 0, 5); // Limits for sigma
    fConvolutedFit->SetParNames("Offset", "Swing", "Mu", "Sigma");
    // Restrict the fit range using SetRange
    fConvolutedFit->SetRange(0, 9);// * 0.3); // Set range from 0 to 8 * 0.3
    // Fit the function to the data in the graph
    misc2->Fit(fConvolutedFit, "R"); // "R" for restricted fit

    misc1->GetXaxis()->SetTitle("Camera Row");
    misc1->GetXaxis()->SetNdivisions(16);
    misc1->GetYaxis()->SetTitle("Average Pedestal RMS [ADC counts]");
    misc1->SetLineWidth(1);
    misc1->SetLineColor(kBlack);
    misc1->SetStats(0);
    
    misc2->SetMarkerStyle(20);
    misc2->SetMarkerColor(kBlack);
    misc2->SetLineColor(kBlack);
    misc2->SetLineWidth(1);

    // Optionally draw the fitted function on the same canvas
    fConvolutedFit->SetLineColor(kRed);
    fConvolutedFit->Draw("same");

    Double_t offset = fConvolutedFit->GetParameter(0);
    Double_t offsetError = fConvolutedFit->GetParError(0);
    Double_t swing = fConvolutedFit->GetParameter(1);
    Double_t swingError = fConvolutedFit->GetParError(1);
    Double_t mu = fConvolutedFit->GetParameter(2);
    Double_t muError = fConvolutedFit->GetParError(2);
    Double_t sigma = fConvolutedFit->GetParameter(3);
    Double_t sigmaError = fConvolutedFit->GetParError(3);
    Double_t chi2 = fConvolutedFit->GetChisquare();
    Int_t ndf = fConvolutedFit->GetNDF(); // Number of degrees of freedom
    pt = new TPaveText(0.6, 0.6, 0.9, 0.9, "NDC"); // NDC: Normalized Device Coordinates
    pt->SetFillColor(0); // Transparent background
    pt->SetTextAlign(12); // Align left
	pt->AddText(Form("Offset: %.3f +/- %.3f [ADC counts]", offset, offsetError));
    pt->AddText(Form("Swing: %.3f +/- %.3f [ADC counts]", swing, swingError));
    pt->AddText(Form("Mu: %.3f +/- %.3f", mu, muError));
    pt->AddText(Form("Sigma: %.3f +/- %.3f", sigma, sigmaError));
    pt->AddText(Form("#chi^{2}/ndf: %.2f / %d", chi2, ndf));

    t_disp->cd();
    misc1->Draw("hist");
    misc2->Draw("P same");
    pt->Draw();

    psfSigma = sigma;
}

// get values functions
vector<vector<int>> DataSummary::GetTrTh(){
    return trTh;
}
double DataSummary::GetAvgEv(){
    return avgEv;
}
double DataSummary::GetAmpDist(){
    return ampDist;
}
double DataSummary::GetHLEDMean(){
    return hledMean;
}
double DataSummary::GetHLEDNMean(){
    return hledNMean;
}
double DataSummary::GetPedMean(){
    return pedMean;
}
double DataSummary::GetPedRMSMean(){
    return pedRMSMean;
}
double DataSummary::GetqMean(){
    return qMean;
}
double DataSummary::GetPTMean(){
    return ptMean;
}
double DataSummary::GetPSFSigma(){
    return psfSigma;
}

bool DataSummary::hasData(){
    return isData;
}