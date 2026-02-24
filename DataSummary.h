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
		//split
		double avgEv44;
		double avgEv415;

		//split
		double ampDist44;
		double ampDist415;

		//split
		double hledMean44;
		double hledNMean44;
		double pedMean44;
		double pedRMSMean44;
		double ampMean44;
		double qMean44;
		double ptMean44;

		double hledMean415;
		double hledNMean415;
		double pedMean415;
		double pedRMSMean415;
		double ampMean415;
		double qMean415;
		double ptMean415;
		//

		double psfSigma;
		vector<vector<int>> trTh;

		//split
		vector<DtStruct> testEv44;
		vector<DtStruct> hledEv44;
		vector<DtStruct> testEv415;
		vector<DtStruct> hledEv415;
		

		vector<vector<Double_t>> pixMeans;

		//split
		vector<Double_t> meanPedRMS44;
		vector<Double_t> meanPedRMS415;

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
		
		//
		bool isData44;
		bool isData415;
		//

		void ReadEv(string readStr);

		//changed to IEvent
		bool isHLED(IEvent *&ev);

		//changed and split
		void AddTestEv44(IEvent *&ev);
		void AddHLEDEv44(IEvent *&ev);
		void AddTestEv415(IEvent *&ev);
		void AddHLEDEv415(IEvent *&ev);

		void ReadTrThresholds(string readStr);
		void FillCamera(int dp);
		void FillDt(int dp);
		void PlotAverages(int dp);
		void FillTrig();
	public:
		TCanvas *t_disp;
		DataSummary(char* dateStr);

		bool hasData();
		//
		bool hasData44();
		bool hasData415();
		//

		void PlotTrig();
		void PlotROIMusic();

		//split
		void PlotFF44();
		void PlotFF415();

		//split
		void PlotHLED44();
		void PlotHLEDNorm44();
		void PlotPedestal44();
		void PlotPedestalRMS44();
		void PlotAmplitude44();
		void PlotCharge44();
		void PlotTimePeak44();

		void PlotHLED415();
		void PlotHLEDNorm415();
		void PlotPedestal415();
		void PlotPedestalRMS415();
		void PlotAmplitude415();
		void PlotCharge415();
		void PlotTimePeak415();
		//

		//split
		void PlotPSF44();
		void PlotPSF415();

		vector<vector<int>> GetTrTh();
		
		//split
		double GetAvgEv44();
		double GetAvgEv415();

		//split
		double GetAmpDist44();
		double GetAmpDist415();

		//split
		double GetHLEDMean44();
		double GetHLEDNMean44();
		double GetPedMean44();
		double GetPedRMSMean44();
		double GetqMean44();
		double GetPTMean44();

		double GetHLEDMean415();
		double GetHLEDNMean415();
		double GetPedMean415();
		double GetPedRMSMean415();
		double GetqMean415();
		double GetPTMean415();
		//

		double GetPSFSigma();
};

#endif