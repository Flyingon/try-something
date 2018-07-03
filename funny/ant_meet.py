import random

"""
int main()
{
    int L,n;
    double pos;
    cin>>L>>n;
    double minT=0,maxT=0;
    for(int i=0;i<n;i++)
    {
        cin>>pos;
        double temp=min(pos,L-pos);
        minT=max(minT,temp);

        temp=max(pos,L-pos);
        maxT=max(maxT,temp);
    }
    cout<<"min="<<minT<<endl;
    cout<<"max="<<maxT<<endl;
    return 0;
}
"""
L = 10
n = 100

def main():
    minT, maxT = 0, 0
    for i in range(0, n):
        pos = random.randint(0, 10)
        print(pos)
        temp = min(pos,L-pos);
        minT = max(minT, temp);
        temp = max(pos, L - pos);
        maxT = max(maxT, temp);
    print("min: ", minT)
    print("max: ", maxT)

if __name__ == '__main__':
    main()