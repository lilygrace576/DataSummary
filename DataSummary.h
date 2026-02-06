#ifndef DataSummary_H
#define DataSummary_H

#include "DtStruct.h"

#include <TROOT.h>
#include <TH2.h>
#include <TH1.h>
#include <TF1.h>
#include <TGraph.h>
#include <TCanvas.h>
#include <TLine.h>
#include <TLegend.h>
#include <TPaveText.h>

//changed to IEvent
#include <IEvent.h>

#include <vector>
#include <cmath>

using namespace std;

class DataSummary {
	private:
		double avgEv;
		double ampDist;
		double hledMean;
		double hledNMean;
		double pedMean;
		double pedRMSMean;
		double ampMean;
		double qMean;
		double ptMean;
		double psfSigma;
		vector<vector<int>> trTh;

		//split
		vector<DtStruct> testEv44;
		vector<DtStruct> hledEv44;
		vector<DtStruct> testEv41_5;
		vector<DtStruct> hledEv41_5;
		//

		vector<vector<Double_t>> pixMeans;
		vector<Double_t> meanPedRMS;
		TF1 *fConvolutedFit;
		TH2F *camera;
		TH2F *ddt;
		TH2F *addt;
		TH1F *trig;
		TH1F *misc1;
		TGraph *misc2;
		TLine *lin;
		TLegend *leg;
		TPaveText *pt;
		bool isData;
		void ReadEv(string readStr);

		//changed to IEvent
		bool isHLED(IEvent *&ev);
		//changed and split
		void AddTestEv44(IEvent *&ev);
		void AddHLEDEv44(IEvent *&ev);
		void AddTestEv41_5(IEvent *&ev);
		void AddHLEDEv41_5(IEvent *&ev);
		//

		void ReadTrThresholds(string readStr);
		void FillCamera(int dp);
		void FillDt(int dp);
		void PlotAverages(int dp);
		void FillTrig();
	public:
		TCanvas *t_disp;
		DataSummary(char* dateStr);
		bool hasData();
		void PlotTrig();
		void PlotROIMusic();
		void PlotFF();

		//split
		void PlotHLED44();
		void PlotHLEDNorm44();
		void PlotPedestal44();
		void PlotPedestalRMS44();
		void PlotAmplitude44();
		void PlotCharge44();
		void PlotTimePeak44();

		void PlotHLED41_5();
		void PlotHLEDNorm41_5();
		void PlotPedestal41_5();
		void PlotPedestalRMS41_5();
		void PlotAmplitude41_5();
		void PlotCharge41_5();
		void PlotTimePeak41_5();
		//

		void PlotPSF();
		vector<vector<int>> GetTrTh();
		double GetAvgEv();
		double GetAmpDist();

		//split
		double GetHLEDMean44();
		double GetHLEDNMean44();
		double GetPedMean44();
		double GetPedRMSMean44();
		double GetqMean44();
		double GetPTMean44();
		double GetPSFSigma44();

		double GetHLEDMean41_5();
		double GetHLEDNMean41_5();
		double GetPedMean41_5();
		double GetPedRMSMean41_5();
		double GetqMean41_5();
		double GetPTMean41_5();
		//

		double GetPSFSigma();
};

#endif