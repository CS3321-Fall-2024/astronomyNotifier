using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AstronomyNotifierUI
{
    public partial class AstronomyNotifierForm : Form
    {
        public AstronomyNotifierForm()
        {
            InitializeComponent();
        }

        private void AstronomyNotifierForm_Load(object sender, EventArgs e)
        {
            setAsteroids();
            setMoonPhases();
            setISS();
            setAuroraAlert();
            setTemps();
        }

        private void setAsteroids()
        {
            string name1 = "Quetzalcoatl"; string mag1 = "18.38"; string dist1 = "3789658.286758657 km";
            string name2 = "Amor"; string mag2 = "17.38"; string dist2 = "27512650.007474516 km";
            string name3 = "Cerberus"; string mag3 = "16.79"; string dist3 = "49946927.092249264 km";
            string name4 = "Icarus"; string mag4 = "16.55"; string dist4 = "12638584.486877465 km";
            string name5 = "Apollo"; string mag5 = "16.08"; string dist5 = "39948089.487965246 km";
            string name6 = "Anteros"; string mag6 = "15.7"; string dist6 = "61713948.434511503 km";
            string name7 = "Albert"; string mag7 = "15.59"; string dist7 = "255628984.281142028 km";
            string name8 = "Antinous"; string mag8 = "15.45"; string dist8 = "13378690.522801436 km";
            string name9 = "Geographos"; string mag9 = "15.27"; string dist9 = "5071250.179154606 km";
            string name10 = "Boreas"; string mag10 = "14.95"; string dist10 = "58321464.907990837 km";
            string name11 = "Daedalus"; string mag11 = "14.86"; string dist11 = "22024826.472922427 km";
            string name12 = "Betulia"; string mag12 = "14.68"; string dist12 = "72648889.115360183 km";
            string name13 = "Cuyo"; string mag13 = "14.41"; string dist13 = "16872246.828310628 km";
            string name14 = "Toro"; string mag14 = "14.28"; string dist14 = "26483638.889510401 km";
            string name15 = "Alinda"; string mag15 = "13.84"; string dist15 = "20461812.339064373 km";
            string name16 = "Ivar"; string mag16 = "12.83"; string dist16 = "24911351.782082527 km";
            string name17 = "Sisyphus"; string mag17 = "12.5"; string dist17 = "67489009.737963225 km";
            string name18 = "Eros"; string mag18 = "10.41"; string dist18 = "47112732.928149391 km";
            string name19 = "Ganymed"; string mag19 = "9.2"; string dist19 = "292651826.06856319 km";

            Label[] astrdNames = { astrd1NameLbl, astrd2NameLbl, astrd3NameLbl, astrd4NameLbl, astrd5NameLbl, astrd6NameLbl, astrd7NameLbl, astrd8NameLbl, astrd9NameLbl,
            astrd10NameLbl, astrd11NameLbl, astrd12NameLbl, astrd13NameLbl, astrd14NameLbl, astrd15NameLbl, astrd16NameLbl, astrd17NameLbl, astrd18NameLbl, astrd19NameLbl};
            Label[] astrdMags = { astrd1MagLbl, astrd2MagLbl, astrd3MagLbl, astrd4MagLbl, astrd5MagLbl, astrd6MagLbl, astrd7MagLbl, astrd8MagLbl, astrd9MagLbl,
                astrd10MagLbl, astrd11MagLbl, astrd12MagLbl, astrd13MagLbl, astrd14MagLbl, astrd15MagLbl, astrd16MagLbl, astrd17MagLbl, astrd18MagLbl, astrd19MagLbl};
            Label[] astrdDists = { astrdDistLbl1, astrdDistLbl2, astrdDistLbl3, astrdDistLbl4, astrdDistLbl5, astrdDistLbl6, astrdDistLbl7, astrdDistLbl8, astrdDistLbl9,
                astrdDistLbl10, astrdDistLbl11, astrdDistLbl12, astrdDistLbl13, astrdDistLbl14, astrdDistLbl15, astrdDistLbl16, astrdDistLbl17, astrdDistLbl18, astrdDistLbl19};

            string[] astrdNamesArr = { name1, name2, name3, name4, name5, name6, name7, name8, name9, name10, name11, name12, name13, name14, name15, name16, name17, name18, name19 };
            string[] astrdMagsArr = { mag1, mag2, mag3, mag4, mag5, mag6, mag7, mag8, mag9, mag10, mag11, mag12, mag13, mag14, mag15, mag16, mag17, mag18, mag19 };
            string[] astrdDistsArr = { dist1, dist2, dist3, dist4, dist5, dist6, dist7, dist8, dist9, dist10, dist11, dist12, dist13, dist14, dist15, dist16, dist17, dist18, dist19 };

            for (int i = 0; i < astrdNames.Length; i++)
            {
                astrdNames[i].Text = astrdNamesArr[i];
                astrdMags[i].Text = astrdMagsArr[i];
                astrdDists[i].Text = astrdDistsArr[i];
            }
        }

        private void setMoonPhases()
        {
            string day1 = "Waxing Crescent";
            string day2 = "Waxing Crescent";
            string day3 = "Waxing Crescent";
            string day4 = "Waxing Crescent";
            string day5 = "Waxing Crescent";
            string day6 = "Waxing Crescent";
            string day7 = "Waxing Crescent";

            string[] days = { day1, day2, day3, day4, day5, day6, day7 };
            PictureBox[] moonPhases = { moonPhasePic1, moonPhasePic2, moonPhasePic3, moonPhasePic4, moonPhasePic5, moonPhasePic6, moonPhasePic7 };
            int day = 0;
            foreach (PictureBox phase in moonPhases)
            {
                switch (days[0])
                {
                    case "First Quarter":
                        phase.Image = Properties.Resources.firstQuarter;
                        break;
                    case "Full Moon":
                        phase.Image = Properties.Resources.fullMoon;
                        break;
                    case "Last Quarter":
                        phase.Image = Properties.Resources.lastQuarter;
                        break;
                    case "New Moon":
                        phase.Image = Properties.Resources.newMoon;
                        break;
                    case "Waning Crescent":
                        phase.Image = Properties.Resources.waningCrescent;
                        break;
                    case "Waning Gibbous":
                        phase.Image = Properties.Resources.waningGibbous;
                        break;
                    case "Waxing Crescent":
                        phase.Image = Properties.Resources.waxingCrescent;
                        break;
                    case "Waxing Gibbous":
                        moonPhasePic1.Image = Properties.Resources.waxingGibbous;
                        break;
                }
                day++;
            }
        }

        private void setISS()
        {
            string date = "2024-12-02";
            string distance = "11673.26 kilometers";
            issNextPassLbl.Text = date;
            issDistanceLbl.Text = distance;
        }

        private void setAuroraAlert()
        {
            string visible = "Not Visible";
            auroraAlertLbl.Text = visible;
        }

        private void setTemps()
        {
            string day1 = "Monday"; string high1 = "46.9 F"; string low1 = "24.1 F";
            string day2 = "Tuesday"; string high2 = "49.1 F"; string low2 = "25.7 F";
            string day3 = "Wednesday"; string high3 = "42.4 F"; string low3 = "28.0 F";
            string day4 = "Thursday"; string high4 = "44.6 F"; string low4 = "28.7 F";
            string day5 = "Friday"; string high5 = "39.2 F"; string low5 = "33.9 F";
            string day6 = "Saturday"; string high6 = "44.0 F"; string low6 = "33.7 F";
            string day7 = "Sunday"; string high7 = "37.3 F"; string low7 = "29.6 F";

            Label[] days = { weekDay1, weekDay2, weekDay3, weekDay4, weekDay5, weekDay6, weekDay7 };
            Label[] highs = { highDay1, highDay2, highDay3, highDay4, highDay5, highDay6, highDay7 };
            Label[] lows = { lowDay1, lowDay2, lowDay3, lowDay4, lowDay5, lowDay6, lowDay7 };

            string[] daysArr = { day1, day2, day3, day4, day5, day6, day7 };
            string[] highsArr = { high1, high2, high3, high4, high5, high6, high7 };
            string[] lowsArr = { low1, low2, low3, low4, low5, low6, low7 };

            for (int i = 0; i < days.Length; i++)
            {
                days[i].Text = daysArr[i];
                highs[i].Text = highsArr[i];
                lows[i].Text = lowsArr[i];
            }
        }
    }
}
