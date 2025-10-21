/**
 * API 客户端 - 前后端数据连接
 */
class LabelSystemAPI {
    constructor(baseURL = 'http://localhost:8000/api/v1') {
        this.baseURL = baseURL;
    }

    /**
     * 发送HTTP请求
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || `HTTP ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error('API请求失败:', error);
            throw error;
        }
    }

    /**
     * 标签管理API
     */
    async getLabels(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/labels?${queryString}`);
    }

    async getLabelById(id) {
        return this.request(`/labels/${id}`);
    }

    async createLabel(labelData) {
        return this.request('/labels', {
            method: 'POST',
            body: JSON.stringify(labelData)
        });
    }

    async updateLabel(id, labelData) {
        return this.request(`/labels/${id}`, {
            method: 'PUT',
            body: JSON.stringify(labelData)
        });
    }

    async deleteLabel(id) {
        return this.request(`/labels/${id}`, {
            method: 'DELETE'
        });
    }

    async getLabelTree(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const qs = queryString ? `?${queryString}` : '';
        return this.request(`/labels/tree${qs}`);
    }

    async getChildrenLabels(labelCode) {
        return this.request(`/labels/${labelCode}/children`);
    }

    /**
     * 规则管理API
     */
    async getRules(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/rules?${queryString}`);
    }

    async getRuleById(id) {
        return this.request(`/rules/${id}`);
    }

    async createRule(ruleData) {
        return this.request('/rules', {
            method: 'POST',
            body: JSON.stringify(ruleData)
        });
    }

    async updateRule(id, ruleData) {
        return this.request(`/rules/${id}`, {
            method: 'PUT',
            body: JSON.stringify(ruleData)
        });
    }

    async deleteRule(id) {
        return this.request(`/rules/${id}`, {
            method: 'DELETE'
        });
    }

    async getRulesByLabelCode(labelCode) {
        return this.request(`/rules/by_label_code/${labelCode}`);
    }

    /**
     * 实体标签管理API
     */
    async getEntityTags(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const qs = queryString ? `?${queryString}` : '';
        return this.request(`/entity_tags/${qs}`);
    }

    async getEntityTagById(id) {
        return this.request(`/entity_tags/${id}`);
    }

    async createEntityTag(entityData) {
        return this.request('/entity_tags/', {
            method: 'POST',
            body: JSON.stringify(entityData)
        });
    }

    async updateEntityTag(id, entityData) {
        return this.request(`/entity_tags/${id}` , {
            method: 'PUT',
            body: JSON.stringify(entityData)
        });
    }

    async deleteEntityTag(id) {
        return this.request(`/entity_tags/${id}`, {
            method: 'DELETE'
        });
    }

    async getEntityTagNames() {
        // 后端未必提供专门的名称列表接口，这里从列表构造
        const list = await this.getEntityTags();
        const data = Array.isArray(list?.data) ? list.data : Array.isArray(list) ? list : [];
        const names = Array.from(new Set(data.map(x => x.entity_tag_name || x.entity_name).filter(Boolean)));
        return { data: names };
    }

    async getEntitiesByTagName(tagName) {
        return this.request(`/entity-tags/tag/${tagName}/entities`);
    }

    /**
     * 意图识别API
     */
    async recognizeIntent(text, context = {}) {
        return this.request('/intent_recognition/recognize', {
            method: 'POST',
            body: JSON.stringify({
                query: text,
                context
            })
        });
    }

    /**
     * 数据项管理API
     */
    async getItems(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/items?${queryString}`);
    }

    async getItemById(id) {
        return this.request(`/items/${id}`);
    }

    async createItem(itemData) {
        return this.request('/items', {
            method: 'POST',
            body: JSON.stringify(itemData)
        });
    }

    async updateItem(id, itemData) {
        return this.request(`/items/${id}`, {
            method: 'PUT',
            body: JSON.stringify(itemData)
        });
    }

    async deleteItem(id) {
        return this.request(`/items/${id}`, {
            method: 'DELETE'
        });
    }

    async getItemsForLabel(labelCode) {
        return this.request(`/items/by_label/${labelCode}`);
    }
}

// 创建全局API实例
window.api = new LabelSystemAPI();

/**
 * 前端数据管理类
 */
class FrontendDataManager {
    constructor() {
        this.api = window.api;
        this.cache = new Map();
    }

    /**
     * 获取标签树数据
     */
    async getLabelTree(params = {}) {
        try {
            const response = await this.api.getLabelTree(params);
            return response?.data ?? response ?? [];
        } catch (error) {
            console.error('获取标签树失败:', error);
            return [];
        }
    }

    /**
     * 根据标签编码获取规则
     */
    async getRulesByLabelCode(labelCode) {
        try {
            const response = await this.api.getRulesByLabelCode(labelCode);
            return response?.data ?? response ?? [];
        } catch (error) {
            console.error('获取规则失败:', error);
            return [];
        }
    }

    /**
     * 获取实体标签名称列表
     */
    async getEntityTagNames() {
        try {
            const response = await this.api.getEntityTagNames();
            const data = response?.data ?? response ?? [];
            return data;
        } catch (error) {
            console.error('获取实体标签名称失败:', error);
            return [];
        }
    }

    /**
     * 意图识别
     */
    async recognizeIntent(text) {
        try {
            const response = await this.api.recognizeIntent(text);
            return response.data;
        } catch (error) {
            console.error('意图识别失败:', error);
            return null;
        }
    }

    /**
     * 创建规则
     */
    async createRule(ruleData) {
        try {
            const response = await this.api.createRule(ruleData);
            return response.data;
        } catch (error) {
            console.error('创建规则失败:', error);
            throw error;
        }
    }

    /**
     * 更新规则
     */
    async updateRule(ruleId, ruleData) {
        try {
            const response = await this.api.updateRule(ruleId, ruleData);
            return response.data;
        } catch (error) {
            console.error('更新规则失败:', error);
            throw error;
        }
    }

    /**
     * 删除规则
     */
    async deleteRule(ruleId) {
        try {
            await this.api.deleteRule(ruleId);
            return true;
        } catch (error) {
            console.error('删除规则失败:', error);
            throw error;
        }
    }
}

// 创建全局数据管理器实例
window.dataManager = new FrontendDataManager();