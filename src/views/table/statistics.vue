<template>
  <div class="icons-container">
    <el-tabs type="border-card">
      <el-tab-pane label="saving">
        <div class="filter-container">
        <el-select v-model="SavinglistQuery.bank_name" placeholder="bank_name" style="width: 150px;margin-left: 10px" class="filter-item">
            <el-option label="ustc-bank" value="ustc-bank"> </el-option>
            <el-option label="fdu-bank" value="fdu-bank"></el-option>
            <el-option label="nju-bank" value="nju-bank"></el-option>
            <el-option label="pku-bank" value="pku-bank"></el-option>
            <el-option label="zju-bank" value="zju-bank"></el-option>
        </el-select>
        <!-- <el-input v-model="SavinglistQuery.bank_name" placeholder="ustc-bank" style="width: 150px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleSavingFilter" /> -->
        <el-select v-model="SavinglistQuery.filter" placeholder="month" style="width: 150px;margin-left: 10px" class="filter-item">
            <el-option label="month" value="month"> </el-option>
            <el-option label="season" value="season"></el-option>
            <el-option label="year" value="year"></el-option>
        </el-select>
        <el-button v-waves class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-search" @click="handleSavingFilter">
            Select
        </el-button>
        </div>
        <el-table
            :key="tableKey"
            v-loading="listLoading"
            :data="saving_list"
            border
            fit
            highlight-current-row
            style="width: 100%;"
        >
            <el-table-column label="bank_name" prop="bank_name" align="center" width="width * 25%">
            <template slot-scope="{row}">
                <span>{{ row[0] }}</span>
            </template>
            </el-table-column>
            <el-table-column label="date" prop="date" align="center" width="width * 25%">
            <template slot-scope="{row}">
                <span>{{ row[1] }}</span>
            </template>
            </el-table-column>
            <el-table-column label="balance" prop="balance" align="center" width="width * 25%">
            <template slot-scope="{row}">
                <span>{{ row[2] }}</span>
            </template>
            </el-table-column>
            <el-table-column label="custom" prop="custom" align="center" width="width * 25%">
            <template slot-scope="{row}">
                <span>{{ row[3] }}</span>
            </template>
            </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="loan">
        <div class="filter-container">
        <!-- <el-input v-model="LoanlistQuery.bank_name" placeholder="ustc-bank" style="width: 150px;margin-left: 10px;" class="filter-item" @keyup.enter.native="handleLoanFilter" /> -->
        <el-select v-model="LoanlistQuery.bank_name" placeholder="bank_name" style="width: 150px;margin-left: 10px" class="filter-item">
            <el-option label="ustc-bank" value="ustc-bank"> </el-option>
            <el-option label="fdu-bank" value="fdu-bank"></el-option>
            <el-option label="nju-bank" value="nju-bank"></el-option>
            <el-option label="pku-bank" value="pku-bank"></el-option>
            <el-option label="zju-bank" value="zju-bank"></el-option>
        </el-select>
        <el-select v-model="LoanlistQuery.filter" placeholder="month" style="width: 150px;margin-left: 10px" class="filter-item">
            <el-option label="month" value="month"> </el-option>
            <el-option label="season" value="season"></el-option>
            <el-option label="year" value="year"></el-option>
        </el-select>
        <el-button v-waves class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-search" @click="handleLoanFilter">
            Select
        </el-button>
        </div>
        <el-table
            :key="tableKey"
            v-loading="listLoading"
            :data="loan_list"
            border
            fit
            highlight-current-row
            style="width: 100%;"
        >
            <el-table-column label="bank_name" prop="bank_name" align="center" width="width * 25%">
            <template slot-scope="{row}">
                <span>{{ row[0] }}</span>
            </template>
            </el-table-column>
            <el-table-column label="date" prop="date" align="center" width="width * 25%">
            <template slot-scope="{row}">
                <span>{{ row[1] }}</span>
            </template>
            </el-table-column>
            <el-table-column label="balance" prop="balance" align="center" width="width * 25%">
            <template slot-scope="{row}">
                <span>{{ row[2] }}</span>
            </template>
            </el-table-column>
            <el-table-column label="custom" prop="custom" align="center" width="width * 25%">
            <template slot-scope="{row}">
                <span>{{ row[3] }}</span>
            </template>
            </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="log file">
        <el-table
            :key="tableKey"
            v-loading="listLoading"
            :data="logfile_list"
            border
            fit
            highlight-current-row
            style="width: 100%;"
        >
            <el-table-column label="bank_name" prop="bank_name" align="center" width="width*20%">
            <template slot-scope="{row}">
                <span>{{ row[0] }}</span>
            </template>
            </el-table-column>
            <el-table-column label="date" prop="date" align="center" width="width*20%">
            <template slot-scope="{row}">
                <span>{{ row[1] }}</span>
            </template>
            </el-table-column>
            <el-table-column label="type" prop="type" align="center" width="width*20%">
            <template slot-scope="{row}">
                <span>{{ row[2] }}</span>
            </template>
            </el-table-column>
            <el-table-column label="balance" prop="balance" align="center" width="width*20%">
            <template slot-scope="{row}">
                <span>{{ row[3] }}</span>
            </template>
            </el-table-column>
            <el-table-column label="custom" prop="custom" align="center" width="width*20%">
            <template slot-scope="{row}">
                <span>{{ row[4] }}</span>
            </template>
            </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import clipboard from '@/utils/clipboard'
import { get_logfile, get_saving_record, get_loan_record } from '@/api/statistics'
import data from '../pdf/content'
// import svgIcons from './svg-icons'
// import elementIcons from './element-icons'

export default {
  name: 'Statistics',
  directives: { waves },
  data() {
    return {
      listLoading: true,
      tableKey: 0,
      saving_list: null,
      loan_list: null,
      logfile_list: null,
      SavinglistQuery: {
        bank_name: '',
        filter: ''
      },
      LoanlistQuery: {
        bank_name: '',
        filter: ''
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      get_logfile().then(response => {
        console.log('get logfile data')
        console.log(response.data)
        this.logfile_list = response.data
        // this.total = response.data.total
        this.listLoading = false
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
      var data = {
          bank_name: 'ustc-bank',
          filter: 'season'
      }
      get_saving_record(data).then(response => {
        console.log('get saving data')
        console.log(response.data)
        this.saving_list = response.data
        // this.total = response.data.total
        this.listLoading = false
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
      get_loan_record(data).then(response => {
        console.log('get loan data')
        console.log(response.data)
        this.loan_list = response.data
        // this.total = response.data.total
        this.listLoading = false
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleLoanFilter() {
        var data = {
            bank_name: this.LoanlistQuery.bank_name,
            filter: this.LoanlistQuery.filter
        }
        get_loan_record(data).then(response => {
        console.log('get loan data')
        console.log(response.data)
        this.loan_list = response.data
        // this.total = response.data.total
        this.listLoading = false
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleSavingFilter() {
        var data = {
            bank_name: this.SavinglistQuery.bank_name,
            filter: this.SavinglistQuery.filter
        }
        get_saving_record(data).then(response => {
            console.log('get saving data')
            console.log(response.data)
            this.saving_list = response.data
            // this.total = response.data.total
            this.listLoading = false
            // Just to simulate the time of the request
            setTimeout(() => {
                this.listLoading = false
            }, 1.5 * 1000)
        })
    },
    generateIconCode(symbol) {
      return `<svg-icon icon-class="${symbol}" />`
    },
    generateElementIconCode(symbol) {
      return `<i class="el-icon-${symbol}" />`
    },
    handleClipboard(text, event) {
      clipboard(text, event)
    }
  }
}
</script>

<style lang="scss" scoped>
.icons-container {
  margin: 10px 20px 0;
  overflow: hidden;

  .grid {
    position: relative;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }

  .icon-item {
    margin: 20px;
    height: 85px;
    text-align: center;
    width: 100px;
    float: left;
    font-size: 30px;
    color: #24292e;
    cursor: pointer;
  }

  span {
    display: block;
    font-size: 16px;
    margin-top: 10px;
  }

  .disabled {
    pointer-events: none;
  }
}
</style>
