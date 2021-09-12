#include <bits/stdc++.h>

#include "DeepSOM.cpp"
#include "Eigen/Dense"
#include "Map2d.cpp"
#include "MapHex.cpp"
#include "MapRect.cpp"
#include "Node.cpp"
#include "SOM.cpp"

using namespace std;

using Eigen::Map;
using Eigen::Vector2d;

vector<VectorXd> read_data(string file_name) {
    vector<VectorXd> datas;
    double buff[1000];
    ifstream infile;
    infile.open(file_name);
    string line;
    int num, length;
    infile >> num >> length;
    datas.reserve(length);
    while (!infile.eof()) {
        getline(infile, line);
        int str_num = 0;
        stringstream stream(line);
        while (!stream.eof()) {
            stream >> buff[str_num++];
        }
        if (str_num != num) {
            continue;
        }
        datas.emplace_back(str_num);
        for (int i = 0; i < num; i++) {
            datas.back()(i) = buff[i];
        }
    }
    infile.close();
    return datas;
}

VectorXd combine(vector<VectorXd> vecs) {
    int total_size = 0;
    for (VectorXd& vec : vecs) {
        total_size += vec.size();
    }
    VectorXd vec_joined(total_size);
    Eigen::CommaInitializer<VectorXd> factory = vec_joined << VectorXd(0);
    for (VectorXd& vec : vecs) {
        factory, vec;
    }
    return vec_joined;
}

VectorXd get_data(VectorXd& data, int id_v) {
    return data.segment(id_v, 2);
}

VectorXd get_output(SOM& som, VectorXd& data_vec) {
    return som.find_bmu(data_vec).get_pos();
}

int main() {
    DeepSOM ds(10);

    int a = ds.add_SOM<MapRect>(10, -1, vector<int>(10, 10));
    ds.set_get_data(a, [](VectorXd& data) -> VectorXd { return get_data(data, 0); });
    int b = ds.add_SOM<MapRect>(10, -1, vector<int>(10, 10));
    ds.set_get_data(b, [](VectorXd& data) -> VectorXd { return get_data(data, 1); });
    int c = ds.add_SOM<MapRect>(10, -1, vector<int>(10, 10));
    ds.set_get_output(c, get_output);
    ds.set_combine(c, combine);

    int d = ds.add_SOM<MapRect>(10, -1, vector<int>(10, 10));
    ds.set_get_output(d, get_output);
    ds.set_combine(d, combine);

    int e = ds.add_SOM<MapRect>(10, -1, vector<int>(10, 10));
    ds.set_get_output(e, get_output);
    ds.set_combine(e, combine);


    ds.add_link(a, c);
    ds.add_link(b, c);

    ds.add_link(a, d);
    ds.add_link(b, d);

    ds.add_link(c, e);
    ds.add_link(d, e);


    vector<VectorXd> data = read_data("modified.txt");
    ds.batch_train(data);
    for(auto& d : data){
        cout << ds.test(d) << endl;
    }
    
}