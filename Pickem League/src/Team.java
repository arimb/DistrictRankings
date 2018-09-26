public class Team {

    public String number;
    public int price;
    public double DP;

    public Team(String number, int price, double DP){
        this.number = number;
        this.price = price;
        this.DP = DP;
    }

    public String toString(){
        return number;
    }

}
