import java.util.*;
import java.io.File;

public class PickemLeague {

    private static ArrayList<Team> best;
    private static double bestTotal;

    public static void main(String[] args){

        HashMap<String, Double> allteams = new HashMap<>();
        String[] line;
        try {
            Scanner dpreader = new Scanner(new File("2018_world_DP.csv"));
            dpreader.nextLine();
            while(dpreader.hasNext()){
                line = dpreader.nextLine().trim().split(",");
                allteams.put(line[0], Double.parseDouble(line[8]));
            }
        }catch(Exception e) {
            e.printStackTrace();
        }

        ArrayList<Team> teams = new ArrayList<Team>();
        try {
            Scanner reader = new Scanner(new File("input.csv"));
            reader.nextLine();
            while(reader.hasNext()){
                line = reader.nextLine().trim().split(",");
                teams.add(new Team(line[0], Integer.parseInt(line[1]), allteams.get(line[0])));
            }
        }catch(Exception e) {
            e.printStackTrace();
        }

//        for(Team x : teams){
//            System.out.println(x.number + ", " + x.price + ", " + x.DP);
//        }

        best = new ArrayList<Team>();
        bestTotal = 0;
        generate(new ArrayList<Team>(), teams, 200);
        System.out.println(best);
        System.out.println(bestTotal);

    }

    private static void generate(ArrayList<Team> current, ArrayList<Team> lst, int shekels) {
        int currentPrice = 0;
        double currentDP = 0;
        for (Team x : current) {
            currentPrice += x.price;
            currentDP += x.DP;
        }

        for (Team team : lst) {
            if (current.size() == 1) System.out.println(current.toString() + team.number);
            if (currentPrice + team.price <= shekels) {
                if (currentDP + team.DP > bestTotal) {
                    best = new ArrayList<Team>(current);
                    best.add(team);
                    bestTotal = currentDP + team.DP;
                    System.out.println(best + ", " + bestTotal);
                }
                if (lst.size() > 1) {
                    ArrayList<Team> newCurrent = new ArrayList<>(current);
                    newCurrent.add(team);
                    ArrayList<Team> newLst = new ArrayList<>(lst);
                    while(newLst.get(0) != team) newLst.remove(0);
                    newLst.remove(0);
                    generate(newCurrent, newLst, shekels);
                }
            }
        }
    }
}
