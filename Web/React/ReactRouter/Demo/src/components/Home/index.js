import React, { Component } from "react";

class Home extends Component {
  render() {
    console.info('类组件：', this.props);
    return (
      <div>
        <h2>Home</h2>
      </div>
    );
  }
}

export default Home;
